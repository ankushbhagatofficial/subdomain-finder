import requests
import json
import os, sys, signal
import time
import logging
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn
from rich.logging import RichHandler
from rich.console import Console
from rich.align import Align
from rich.panel import Panel
from rich.syntax import Syntax
from rich.traceback import install
install()

# Define a signal handler for SIGTSTP and SIGTSTP
def signal_handler(signal, frame):
#    print("Program exit.")
    sys.stdout.write('\rProgram exit.                           ')
    sys.stdout.flush()
    print()
    sys.exit()

signal.signal(signal.SIGTSTP, signal_handler)
signal.signal(signal.SIGINT, signal_handler)


FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")

console = Console()

try:
    api = os.environ["SD_API_KEY"]
except Exception:
    bash_syntax = Syntax("export SD_API_KEY=\"api_key_value\"", "bash")
    win_syntax = Syntax("setx [SD_API_KEY] \"[api_key_value]\"", "powershell")
    console.print("Set \"SD_API_KEY\" Environment Variable:")
    console.print("For Linux/Macos:", bash_syntax)
    console.print("For Windows:", win_syntax)
    sys.exit(1)

def get_sub_domains(domain,filepath):
    domain = domain.replace("https://", "").replace("http://", "").replace("/", "").replace("www.", "")
    try:
        response = requests.get('http://'+domain)
        if response.status_code == 200:
            log.info(f"Valid URL: http://{domain}")
        else:
            log.info(f"Invalid URL: http://{domain}")
            sys.exit(1)
    except requests.exceptions.InvalidURL:
        log.info(f"Invalid URL: http://{domain}")
        sys.exit(1)

    url = "https://api.securitytrails.com/v1/domain/"+domain+"/subdomains"
    #print(url)
    querystring = {"children_only":"true"}
    headers = {
    'accept': "application/json",
    'apikey': api
    }
    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.status_code == 429:
        log.critical("You reached your quota or rate limit; see Quotas & Rate Limits.\nhttps://docs.securitytrails.com/docs/quotas-rate-limits")
        sys.exit(1)

    elif response.status_code == 403:
        log.error("The requested information can not be accessed.")
        sys.exit(1)

    elif response.status_code == 401:
        log.error("You did not provide a valid API key; see Authentication.\nhttps://docs.securitytrails.com/docs/authentication")
        sys.exit(1)

    elif response.status_code == 500:
        log.error("An internal error occurred. In case the error persists, please contact our support.\nhttps://docs.securitytrails.com/docs/contact-support")
        sys.exit(1)

    f = open(filepath, 'w')
    f.write("")

    result_json=json.loads(response.text)
    with Progress(
    SpinnerColumn(),
    *Progress.get_default_columns(),
    TimeElapsedColumn(),
    transient=True,
) as progress:
        task = progress.add_task(f"[yellow][Saving to]: '{filepath}'", total=None)
        n = 0
        for i in result_json['subdomains']:
            log.info(i+'.'+domain)
            n += 1
            f = open(filepath, 'a')
            f.write(i+'.'+domain+'\n')
            time.sleep(0.020)
    f.close()
    console.print(f"([bold blue]TOTAL[/]: {n}) \[[u]subdomains saved to[/]]: [bold green]{filepath}")
#        sub_domains=[i+'.'+domain for i in result_json['subdomains']]
#    return sub_domains

def center_align(text, subtitle, width):
    align_center = Panel(Align(text, align="center"), subtitle=subtitle, width=width)
    console.print(align_center, justify="center")

width, height = console.size

banner = """[blue]┏━┓╻ ╻┏┓ ╺┳┓┏━┓┏┳┓┏━┓╻┏┓╻   ┏━╸╻┏┓╻╺┳┓┏━╸┏━┓
┗━┓┃ ┃┣┻┓ ┃┃┃ ┃┃┃┃┣━┫┃┃┗┫╺━╸┣╸ ┃┃┗┫ ┃┃┣╸ ┣┳┛
┗━┛┗━┛┗━┛╺┻┛┗━┛╹ ╹╹ ╹╹╹ ╹   ╹  ╹╹ ╹╺┻┛┗━╸╹┗╸"""

def arg_error():
    program_name = sys.argv[0]
    center_align(f"[u b blue]{program_name}[/]: [b green]try[/] [b]'{program_name} --help'[/]", f"[u b blue]{program_name}[/]: [b red]argument[/] [b]'{sys.argv[1]}' not found[/]", None)
    sys.exit(1)

def gethelp():
    program_name = sys.argv[0]
    console.print(f"""usage {program_name}:
   --domain   [yellow]\[name_of_domain][/]   [b green]specify a domain name[/]
   --filepath [yellow]\[saveto_filename][/]  [b green]specify filename where to save[/]

e.g:
{program_name} --domain [u blue]facebook.com[/] --filepath [green]fb_sd.txt[/]""")
    center_align("[b green]Program by", "Ankush Bhagat", width-40)
    sys.exit(1)

try:
    if sys.argv[1] == "--help":
        gethelp()
    if len(sys.argv) > 1 and not sys.argv[1] == "--domain":
                arg_error()
    elif sys.argv[1] == "--domain":
        if len(sys.argv) >= 3:
            arg_domain = sys.argv[2]
#            print("got domain")
            if len(sys.argv) <= 3:
                center_align("[b red]--filepath argument missing", "[b green]use: --filepath", None)
                sys.exit(1)
        else:

            center_align("[b red]domain name missing", "[b green]e.g: [u]example.com[/]", None)
            sys.exit(1)

    if sys.argv[3] == "--filepath":
        if len(sys.argv) >= 5:
            arg_filepath = sys.argv[4]
#            print("got filepath")
        else:
            center_align("[b red]filepath missing", "[b green]e.g: [u]file.txt[/]", None)
            sys.exit(1)

#    if sys.argv[5] == "expert_mode="*:
#        print()
#        exit()

except Exception:
    pass
#    filepath = sys.argv[2]

try:
    domain = arg_domain
    filepath = arg_filepath
except Exception:
    center_align(banner, "[b u yellow]https://github.com/ankushbhagatofficial/subdomain-finder", 62)
    domain=console.input(f"""\ne.g ([u]example.com[/])
\[[b blue]Enter a Domain Name[/]]: """)
    filepath=console.input("\[[b green]Provide filepath to save sudomains[/]]: ")
get_sub_domains(domain,filepath)

