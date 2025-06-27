import requests as rq, json as js, sys as sy
from colorama import init as i, Fore as F
from rich.console import Console as C
from rich.table import Table as T
from rich.progress import track as tr
from PIL import Image as I, ImageDraw as D, ImageFont as IF
import io as o

i(autoreset=True)
c = C()

def g(d):
    u = f"https://api.hackertarget.com/hostsearch/?q={d}"
    try:
        p = rq.get(u)
        if p.status_code == 200:
            a = []
            for l in p.text.splitlines():
                if l.strip():
                    s, ip = l.split(',')[:2]
                    a.append({"subdomain": s, "ip": ip})
            return a
        else:
            c.print(f"[red]Error:[/red] Gagal mengambil data. Status code: {p.status_code}")
            return None
    except Exception as e:
        c.print(f"[red]Error:[/red] {str(e)}")
        return None

def h(d, s):
    if not s:
        c.print(f"[yellow]Tidak ada subdomain yang ditemukan untuk {d}[/yellow]")
        return
    t = T(title=f"Subdomain dan IP untuk [green]{d}[/green]")
    t.add_column("No.", style="cyan", width=5)
    t.add_column("Subdomain", style="magenta")
    t.add_column("IP Address", style="green")
    t.add_column("Domain Utama", style="yellow")
    for i, x in enumerate(s, 1):
        t.add_row(str(i), x['subdomain'], x['ip'], d)
    c.print(t)
    c.print(f"\n[bold green]Total ditemukan:[/bold green] {len(s)} subdomain")

def b():
    c.print(F.CYAN + "="*60)
    c.print(F.YELLOW + "SUBDOMAIN FINDER TOOL".center(60))
    c.print(F.CYAN + "="*60)
    c.print(F.GREEN + "Menggunakan API dari HackerTarget.com".center(60))
    c.print(F.CYAN + "="*60 + "\n")

def m():
    b()
    d = c.input("[bold yellow]Masukkan domain target (contoh: example.com): [/bold yellow]").strip()
    if not d:
        c.print("[red]Error:[/red] Domain tidak boleh kosong!")
        sy.exit(1)
    c.print(f"\n[bold]Mencari subdomain untuk [green]{d}[/green]...[/bold]\n")
    s = g(d)
    if s:
        h(d, s)
        f = f"subdomains_{d}.json"
        with open(f, 'w') as j:
            js.dump({"domain": d, "subdomains": s}, j, indent=4)
        c.print(f"\n[green]Hasil disimpan ke:[/green] {f}")

if __name__ == "__main__":
    m()
