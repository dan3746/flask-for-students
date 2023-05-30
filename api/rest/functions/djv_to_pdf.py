import glob
import os
import pipes
import shutil
import PyPDF2

# Recursively walks the sexpr tree and outputs a metadata format understandable by pdftk

home = os.path.expanduser("~")

src = ""
dest = ""
tmp = ""

def check_lib():
    assert shutil.which('djvu2hocr'), 'dpsprep requires the djvu2hocr binary, which is part of ocradjvu'
    assert shutil.which('ddjvu') and shutil.which(
        'djvused'), 'dpsprep requires the ddjvu and djvused binaries, which are part of djvulibre'
    assert shutil.which('pdftk'), 'dpsprep requires pdftk'

    if not os.path.exists(home + "/Desktop/books/.dpsprep"):
        os.mkdir(home + "/Desktop/books/.dpsprep")


def make_pdf():
    print("NOTE: Make the PDF, compressing with JPG so they are not ridiculous in size")
    if not os.path.isfile(tmp + '/dumpd'):
        # Пока не удается тут убрать старый формат работы со строками из-за 'pg%%06d.tif'
        retval = os.system("ddjvu -v -eachpage -format=tiff %s %s/pg%%06d.tif" % (src, tmp))
        if retval > 0:
            print("\nNOTE: There was a problem dumping the pages to tiff.  See above output")
            exit(retval)

        print("Flat PDF made.")
        open(tmp + '/dumpd', 'a').close()
    else:
        print("Inflated PDFs already found, using these...")


def dump_file():
    if not os.path.isfile(tmp + '/beadd'):
        cwd = os.getcwd()
        os.chdir(tmp)
        retval = os.system('pdfbeads * > ' + dest)
        if retval > 0:
            print("\nNOTE: There was a problem beading, see above output.")
            exit(retval)

        print("Beading complete.")
        open('beadd', 'a').close()
        os.chdir(cwd)
    else:
        print("Existing destination found, assuming beading already complete...")


def djv_pdf(djv_file):
    global src, dest, tmp

    res = None

    # if djv_file.filename.rsplit('.', 1)[-1] != "djvu":
    #     return res
    # Check libs
    check_lib()

    with open(f'{os.getcwd()}/api/rest/functions/books/{djv_file.filename}', 'wb') as f:
        for chunk in djv_file.iter_content(5):
            f.write(chunk)

        f.write(djv_file.content)

    src = f'{os.getcwd()}/api/rest/functions/books/{djv_file.filename}.djvu'
    dest = f'{os.getcwd()}/api/rest/functions/books/{djv_file.filename}.pdf'
    tmp = home + f'{os.getcwd()}/api/rest/functions/books/.dpsprep'

    src_quote = pipes.quote(src)
    finaldest = pipes.quote(dest)
    dest = home + pipes.quote(dest)



    # Make the PDF, compressing with JPG so they are not ridiculous in size
    # (cwd)
    make_pdf()

    # Is sloppy and dumps to present directory
    dump_file()


    with open(dest, 'rd') as f:
        res = PyPDF2.PdfFileReader(f)

    files = glob.glob(f'{os.getcwd()}/api/rest/functions/books')
    for f in files:
        os.remove(f)

    print("SUCCESS. Temporary files cleared.")

    return res
