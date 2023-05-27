from argparse import ArgumentParser
from pathlib import Path
import asyncio
from tqdm import tqdm
from random import randint
from descriptor import describe_image_fn

async def get_description(image_path):
    # sleep for random second to simulate a blocking operation
    delay = randint(1, 3)
    await asyncio.sleep(delay)
    async with asyncio.timeout(10):
        description = await describe_image_fn(image_path)
    return description


save_path = Path("descriptions")
save_path.mkdir(exist_ok=True, parents=True)

async def index(path):
    path = Path(path)
    if path.is_dir():
        for file in path.iterdir():
            await index(file)
    else:
        descriptions = await get_description(path)
        global save_path

        with open(save_path / (path.stem + ".txt"), "w") as f:
            f.write(descriptions)


def resolve(lsc_root: Path, lsc_filename: str) -> Path:
    year = lsc_filename[:4]
    if year == "2000":
        year = "2019"
        # print(lsc_filename)
        lsc_filename = "2019" + lsc_filename[4:]
    month = lsc_filename[4:6]
    day = lsc_filename[6:8]
    lsc_filename = lsc_filename + ".jpg"
    lsc_dir = lsc_root / f'{year}{month}' / day
    return lsc_dir / lsc_filename

def filter(filename):
    year = filename[:4]
    if int(year) <= 2019:
        return False
    return True

log_folder = Path("logs")
log_folder.mkdir(exist_ok=True, parents=True)

log_path = Path("logs/log.txt")
errors_path = Path("logs/errors.txt")
resume_path = Path("logs/resume.txt")

async def indexlsc(paths_file, lsc_dir, resume_line_idx=0):
    global save_path
    with open(paths_file, "r") as f:
        filenames = f.readlines()
        filenames = filenames[resume_line_idx:]
        for idx, filename in tqdm(enumerate(filenames), total=len(filenames)-resume_line_idx):
            with open(resume_path, "w") as f:
                f.write(str(idx))
            filename = filename.strip()
            if not filter(filename):
                continue
            path = resolve(Path(lsc_dir), filename)
            image_id = path.stem
            try:
                foldername = path.stem[:6]
                assert path.is_file(), "Image does not exist"
                save_descriptions_path = save_path / foldername
                save_descriptions_path.mkdir(exist_ok=True, parents=True)
                save_descriptions_file_path = save_descriptions_path / (path.stem + ".txt")
                assert not save_descriptions_file_path.exists(), "Description file already exists"
                if path.is_dir():
                    for file in path.iterdir():
                        await index(file)
                else:
                    descriptions = await get_description(path)
                    with open(save_descriptions_file_path, "w") as f:
                        f.write(descriptions)
                    with open(log_path, "a") as f:
                        f.write(image_id + "\t" +"Success\t" + str(path) + "\t" + str(save_descriptions_file_path) + "\n")
            except Exception as e:
                with open(errors_path, "a") as f:
                    f.write(image_id + "\t" + str(e) + "\t" + str(path) + "\n")
            
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--lsc-path", type=str, required=True, help="Path to file or directory")
    parser.add_argument("--txt", type=str, required=True, help="Path to image list file")
    parser.add_argument("--resume", type=str, default=None, help="Path to resume file")
    args = parser.parse_args()
    resume_line_idx = 0
    if args.resume:
        resume_path = Path(args.resume)
        assert resume_path.exists(), "Resume path does not exist"
        with open(resume_path, "r") as f:
            resume_line_idx = int(f.read())
    asyncio.run(indexlsc(args.txt, args.lsc_path, resume_line_idx))