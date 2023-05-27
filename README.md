# index-MJ

Generate descriptions for the LSC 23 dataset.
## Usage

```bash
python cli.py --docker mj --port 8081 --channel test --command "python indexlsc.py --lsc lsc23/extracted/ --txt lsc23/images.txt --resume logs/resume.txt"
```