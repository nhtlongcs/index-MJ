from argparse import ArgumentParser
from pathlib import Path
import asyncio
from tqdm import tqdm
from random import randint
from descriptor import describe_image_async as describe_image_fn
import pandas as pd
tqdm.pandas()

MAX_TIMEOUT=30
MAX_IMGS=10000000000

async def get_description(image_path):
    description = None
    # description = await describe_image_fn(image_path)
    delay = randint(0, 1)
    try:
        description = await asyncio.wait_for(describe_image_fn(image_path), timeout=MAX_TIMEOUT)
    except asyncio.exceptions.TimeoutError:
        assert False, "TimeoutError, account maybe temporarily blocked due to suspicious activity, please try again later"
    await asyncio.sleep(delay)
    return description


save_path = Path("descriptions")
save_path.mkdir(exist_ok=True, parents=True)

def filter(filename):
    if filename.startswith("202001"):
        return True
    return False

log_folder = Path("logs")
log_folder.mkdir(exist_ok=True, parents=True)

log_path = Path("logs/log.txt")
errors_path = Path("logs/errors.txt")
resume_path = Path("logs/resume.txt")

def compress(filenames):
    pass # removed for brevity

async def indexlsc2(csv_paths_file, resume_line_idx=0):
    global save_path
    df = pd.read_csv(csv_paths_file)
    df = df[df["image_filename"].apply(filter)]
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        with open(resume_path, "w") as f:
            f.write(str(resume_line_idx + idx))
        path = Path(row["image_path"])
        image_id = path.stem
        try:
            foldername = path.stem[:6]
            assert path.is_file(), "Image does not exist"
            save_descriptions_path = save_path / foldername
            save_descriptions_path.mkdir(exist_ok=True, parents=True)
            save_descriptions_file_path = save_descriptions_path / (path.stem + ".txt")
            assert not save_descriptions_file_path.exists(), "Description file already exists"

            descriptions = await get_description(path)
            assert not (descriptions is None), "Description is None, maybe timeout"
            with open(save_descriptions_file_path, "w") as f:
                f.write(descriptions)
            with open(log_path, "a") as f:
                f.write(image_id + "\t" +"Success\t" + str(path) + "\t" + str(save_descriptions_file_path) + "\n")
        except Exception as e:
            with open(errors_path, "a") as f:
                f.write(image_id + "\t" + str(e) + "\t" + str(path) + "\n")
            if str(e) == "TimeoutError, account maybe temporarily blocked due to suspicious activity, please try again later":
                break
                    
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--csv", type=str, required=True, help="Path to image list file")
    parser.add_argument("--resume", type=str, default=None, help="Path to resume file")
    args = parser.parse_args()
    resume_line_idx = 0
    if args.resume:
        resume_path = Path(args.resume)
        assert resume_path.exists(), "Resume path does not exist"
        with open(resume_path, "r") as f:
            resume_line_idx = int(f.read())

    asyncio.run(indexlsc2(args.csv, resume_line_idx))
