import argparse
from pikwizard import Pikwizard

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='An image downloader for https://pikwizard.com using Selenium. Download royalty free and safe for commercial use images, with no attribution required!')
    parser.add_argument('-s', '--search', type = str, default = 'cute cats', help = 'Search keyword')
    parser.add_argument('-n', '--num_images', type = int, default = 4, help = 'Maximum number of images to download')
    parser.add_argument('-p', '--path', type = str, default = 'downloads', help = 'Directory path to save the images')
    parser.add_argument('-w', '--num_workers', type = int, default = 8, help = 'Number of workers in thread pool')
    parser.add_argument('--height', type = int, default = -1, help = 'Height of downloaded images, -1 : keep original')
    parser.add_argument('--width', type = int, default = -1, help = 'Width of downloaded images, -1 : keep original')
    parser.add_argument('--verbose', action='store_false', help = 'Verbosity')
    args = parser.parse_args()


    pik = Pikwizard(search = args.search, num_images = args.num_images, path = args.path, num_workers = args.num_workers, height = args.height, width = args.width, verbose = args.verbose)
    pik.download()