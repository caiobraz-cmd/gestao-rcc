"""Monta entrega por lista permitida, sem segredos, caches ou ambientes virtuais."""
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
VERSION = '0.5.0-rc1'
FILES = ['README.md', 'CHANGELOG.md', 'requirements.txt', '.env.example', '.gitignore', 'run.py', 'config.py', 'configurar.py', 'INICIAR.cmd']
FOLDERS = ['app', 'templates', 'static', 'tests', 'tools', 'database', 'docs', 'src']
ALLOWED = {'.py', '.md', '.txt', '.html', '.css', '.js', '.json', '.sql', '.png', '.jpg', '.jpeg', '.pdf', '.svg', '.ico'}


def main():
    files = [ROOT / name for name in FILES]
    for folder in FOLDERS:
        files.extend(p for p in (ROOT / folder).rglob('*') if p.is_file() and not p.is_symlink()
                     and '__pycache__' not in p.parts and p.suffix.lower() in ALLOWED and not p.name.startswith('.env'))
    files = sorted(set(files))
    folder = ROOT / 'entrega'
    folder.mkdir(exist_ok=True)
    output = folder / f'gestao-rcc-{VERSION}-candidata.zip'
    manifest = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    with ZipFile(output, 'w', ZIP_DEFLATED) as archive:
        for p in files:
            archive.write(p, p.relative_to(ROOT).as_posix())
        archive.writestr('MANIFESTO-SHA256.json', json.dumps(manifest, ensure_ascii=False, indent=2))
    with ZipFile(output) as archive:
        assert archive.testzip() is None
        for name, expected in manifest.items():
            assert hashlib.sha256(archive.read(name)).hexdigest() == expected
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix('.sha256.txt').write_text(digest + '  ' + output.name + '\n', encoding='utf-8')
    print(f'Pacote verificado: {output}\nArquivos: {len(files)}\nSHA256: {digest}')


if __name__ == '__main__':
    main()
