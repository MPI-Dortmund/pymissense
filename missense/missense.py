import argparse
import gzip
import os
import re
import shutil
import tempfile
import urllib
from urllib.request import urlretrieve

import numpy as np
import requests
from matplotlib import pyplot


def gen_image(pos_to_val) -> np.array:
    unique_to = np.unique([t[1] for t in pos_to_val])[::-1]
    img = np.zeros(shape=(len(unique_to), np.max([p[0] for p in pos_to_val]) + 1))
    for p, t, v in pos_to_val:
        y = np.where(unique_to == t)[0][0]
        x = p
        img[y, x] = v
    return img


def get_data_tuple(uniprot_id: str, max_pos: int = None):
    with open(os.path.join(tempfile.gettempdir(), "alpha.tsv")) as f:
        doc = f.read()
        m = re.findall(uniprot_id.upper() + "\t(.\d+.)\t(\d.\d+)", doc)
    pos_to_val = []

    for g in m:
        position = int(g[0][1:-1])
        if max_pos is not None:
            if position > max_pos:
                break

        to = g[0][-1]
        val = float(g[1])
        pos_to_val.append((position, to, val))

    return pos_to_val

def download_missense_data():
    alphafile=os.path.join(tempfile.gettempdir(), "alpha.tsv")
    if not os.path.exists(alphafile):
        url = ("https://zenodo.org/record/8208688/files/AlphaMissense_aa_substitutions.tsv.gz?download=1/")
        filename = os.path.join(tempfile.gettempdir(), "alpha.tsv.gz")
        print("Download to", filename, " ...")
        urlretrieve(url, filename)
        print("Download done!")
        print("Decompress...")
        with gzip.open(filename,'r') as f_in, open(alphafile, 'wb') as f_out:
            shutil.copyfileobj(f_in,f_out)
        print("Done: ", alphafile)

    else:
        print(f"{alphafile} already exists. Don't download it again.")


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
            description="AlphaMissense plot and pdb generator",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

    parser.add_argument(
        "uniprot_id",
        help="UNIPROT ID",
    )

    parser.add_argument(
        "output_path",
        help="Output folder",
    )

    parser.add_argument(
        "--pdbpath",
        type=str,
        help="If defined, it will write the pathogencity as bfactor in that PDB. If its not defined or not existing it will instead download the alphafold predicted PDB",
        default=None
    )

    parser.add_argument(
        "--maxacid",
        type=int,
        help="Maximum squence number to use.",
        default=None
    )

    return parser


def make_and_save_plot(pos_to_val, out_file: str) -> np.array:
    img = gen_image(pos_to_val)
    fig, ax = pyplot.subplots(1, 1)

    ax.imshow(img, aspect='auto', interpolation='none', cmap="bwr")

    heatmap = ax.pcolor(img, cmap="bwr")
    pyplot.colorbar(heatmap, label="AM Pathogenicity")

    x_label_list = np.unique([p[1] for p in pos_to_val])[::-1]

    yticks = list(range(0, len(np.unique([p[1] for p in pos_to_val]))))
    yticks = [y + 0.5 for y in yticks]
    pyplot.ylim(20, 0)
    ax.set_yticks(yticks)

    ax.set_yticklabels(x_label_list)
    ax.set_ylabel("Alternate amino acid")
    ax.set_xlabel("Residue sequence number")

    pyplot.savefig(out_file, format="pdf", bbox_inches="tight")

    return img

def create_modified_pdb(img: np.array, uniprot_id: str, output_path: str, pdb_pth=None):
    if pdb_pth is not None and os.path.isfile(pdb_pth):
        target_pdb = pdb_pth
    else:
        target_pdb = os.path.join(tempfile.gettempdir(), "AF.pdb")
        api_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id.upper()}"
        response = requests.get(api_url)
        r = response.json()
        urllib.request.urlretrieve(r[0]['pdbUrl'], target_pdb)

    mean_per_pos = img.mean(axis=0)

    with open(target_pdb) as f:
        with open(output_path, 'w+') as out_file:
            for line in f:
                if line.startswith("ATOM "):
                    # find positions here https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/tutorials/pdbintro.html
                    pos = int(line[22:26])
                    value = mean_per_pos[pos]
                    value_str = f"{value:.2f}"
                    while len(value_str) < 6:
                        value_str = " " + value_str
                    edit_line = line[:60] + value_str + line[67:]
                    out_file.write(edit_line)
                else:
                    out_file.write(f'{line}')


def _main_():
    args = create_parser().parse_args()
    download_missense_data()
    os.makedirs(args.output_path, exist_ok=True)

    pos_to_val = get_data_tuple(args.uniprot_id, args.maxacid)

    out_fig_pth = os.path.join(args.output_path, f"{args.uniprot_id}.pdf")
    img_raw_data = make_and_save_plot(pos_to_val, out_fig_pth)
    out_pdb_pth = os.path.join(args.output_path, f'{args.uniprot_id}-edit.pdb')

    create_modified_pdb(img_raw_data, args.uniprot_id, out_pdb_pth, args.pdbpath)


if __name__ == "__main__":
    _main_()