import signac
import sys

from fffit.signac import save_signac_results
from utils.r32 import param_names


def main():
    if len(sys.argv) != 2:
        print("Usage: python extract_r32_density.py [iteration number]")
        exit(1)
    else:
        internum = sys.argv[1]

    run_path = "/scratch365/rdefever/hfcs-fffit/runs/"
    itername = "r32-density-iter1"
    project_path = run_path + itername
    csv_name = "csv/" + itername + ".csv"

    property_names = ["density"]
    project = signac.get_project(project_path)

    save_signac_results(project, param_names(), property_names, csv_name)


if __name__ == "__main__":
    main()
