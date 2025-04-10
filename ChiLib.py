
'''
Big-Picture/ Goal: So in this  project my moto is to locate the Chicago Public Libraries

Use Case: According to the requriemnts of Kartik(hopefully my future project manager =) )
    this customized CLI tool that I am supposed to make, should have a method for retrieving 
    library branch information based on zip code. Which should be designed with proper error handling.
    
My thinking: How I think of this is related through the application demonstration of
             enterprise-grade software engineering principles. 
             Did a project similer to this one in my Object Oriented Pricples course.

The Key Features:
1. data retrieval from official City of Chicago open data repository
2. comrehensivly extracts the information of the library 
3. zip code-based search functionality
4. search history tracking (Bonus Task)
5. logging of errors and its management

My Understanding of Architecture:

1. promoting code reuseablity and maintainance though modular function design 
2. leverages requests library for network operations
3. incorporates CSV parsing to maximize the use of data handling
4. implements real-time data processing with minimal memory cost



'''


# These are all the necessary import statements 
# which will make my CLI program to run smoothly
import sys
import time
import os
import re
import logging
from datetime import datetime
from typing import List, Dict, Any
from io import StringIO
from csv import DictReader

# these are import statements which allow me to present my terminal output 
# in a professional and easy to read format
import pyfiglet
import requests
from rich.console import Console
from rich.table import Table
from rich.progress import Progress



'''
    The main function of the program is to load the libraries from the official City of Chicago open data repository
    and then format the library information in a user-friendly way.

    The user can then search for libraries based on zip code and view the search history.
    I can do that through retrieving library data from the city of Chicago's open data api.


   
    
    My Approach:
    - I want to program with a defensive programming with comprehensive exception handling
    - I should be able to uses StringIO for efficenty using in-memory CSV processing  
    - aslo this should be able to transform raw CSV data into a readily list of dictionaries
    
        expected returns statement:
        list: structured library data or "None" if retrieval fails
    
    Exception Handling:
    - shoud be able to capture and log network-related exceptions
    - makes sure that the program is resilient to inconsistent external data sources.

'''

#  here we will need to initializer a console object from the rich library
console = Console()

# here we need to configure for poduction-grade settings
class Config:
    DATA_URL = os.getenv("LIB_DATA_URL", 
        "https://data.cityofchicago.org/api/views/x8fc-8rcq/rows.csv")
    HISTORY_LIMIT = 100
    ZIP_REGEX = re.compile(r'^[1-9][0-9]{4}$')  # valid zip pattern

# then we will to to plan the production lodgging 
logging.basicConfig(
    filename='library_finder.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# lastly here I will have to error handle
# here I would have to create error handle techniques using three classes 
# I will use LibraryError for exception 
# I will use InvalidZipError for invalid zip code
# I will use DataLoadError for data loading error
class LibraryError(Exception): pass
class InvalidZipError(LibraryError): pass
class DataLoadError(LibraryError): pass



"""
    here I will need to use data loader adhering to 12-factor app principles.
    
    features:
    -------------
    1. timeout management: idea is to prevent system deadlocks with circuit breaker pattern
    2. resource safety: here I will need to use context-managed network connection lifecycle
    3. schema validation: I will need to check the type-enforced response structure
    4. telemetry: this is not needed but this should be able to show detailed observability metrics
    5. error handling: this is also a constant thing in this CLI domain-specific exception hierarchy

    Returns:
    --------
    List[Dict[str, Any]]: here I will need to type-annotated dataset preserving source schema

    """

def load_libraries() -> List[Dict[str, Any]]:
   
    url = Config.DATA_URL
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logger.info("Successfully loaded library data")
        return list(DictReader(StringIO(response.text)))
    except requests.RequestException as e:
        logger.error(f"Data load failed: {str(e)}")
        raise DataLoadError(f"Failed to retrieve library data: {str(e)}")


'''
    transforms raw library data into a readable, formatted string.
    
    have to use advanced formatting strategy:
    1. should be able to dynamically handles optional index for list presentations
    2. shold be able to  manages potential missing data fields
    3. Lastly I can implement defensive programming by using .get() with fallback values
    
    parameters:
        library (dict): is baciacally raw library metadata
        index (int, optional): moves forward with the index for multiple results
    
    returns:
        str: should be able to return or output a really nicely formatted library information
'''

def format_library(library: Dict[str, str], index: int = None) -> str:
    """Format library information with consistent styling"""
    branch_name = library['BRANCH']
    header = f"[bold yellow]🏛️  Library #{index}:[/] [cyan]{branch_name}[/]" if index \
            else f"[bold cyan]🏛️  {branch_name}[/]"
    
    return f"""

    [bold blue]┏{'━'*58}┓[/]
    {header}
    [dim]┃[/] [green]• Hours:[/]    {library.get('SERVICE HOURS', 'Not available')}
    [dim]┃[/] [green]• Address:[/]  {library['ADDRESS']}
    [dim]┃[/]             {library['CITY']}, {library['STATE']} {library['ZIP']}
    [dim]┃[/] [green]• Website:[/]  [link={library['WEBSITE']}]{library['WEBSITE']}[/link]
    [dim]┃[/] [green]• Phone:[/]    {library.get('PHONE', 'N/A').strip()}
    [bold blue]┗{'━'*58}┛[/]
"""


    '''
    should be able to render user's search history with temporal sorting.
    
    optimizing performance:
    1. in this fucntion the major role is to implement a reverse chronological sorting 
       for most recent results first
    2. then after that, minimizes computational complexity with built-in sorted() function
    
    parameters:
        history (list): should output a chronological search record
    '''

def display_history(history: List[Dict]) -> None:
    """Clean history display with screen management"""
    os.system('cls' if os.name == 'nt' else 'clear')
    sorted_entries = sorted(history, key=lambda x: x['time'], reverse=True)
    for entry in sorted_entries:
        console.print(format_library(entry['library']))

# here this will typically be caleed when the user types in like "full history"
# that is wher this function should output the entire history of the user search using timp stamps
def display_history_table(history: List[Dict]) -> None:
    """Professional table display for detailed history"""
    table = Table(title="Search History", show_header=True, header_style="bold magenta")
    table.add_column("Timestamp", style="dim", width=20)
    table.add_column("Library Name", style="cyan")
    table.add_column("ZIP Code", justify="right")
    table.add_column("Phone", width=15)

    for entry in sorted(history, key=lambda x: x['time'], reverse=True):
        lib = entry['library']
        timestamp = entry['time'].strftime("%b %d, %Y\n%I:%M %p")
        table.add_row(timestamp, lib['BRANCH'], lib['ZIP'], lib.get('PHONE', 'N/A'))
    
    console.print(table)


'''
    this main() function where I can make all the function to get like called and use them in the 
    way the project description is. Here I should be able to manage the primary user interaction 
    workflow for searching libraries by ZIP code.

    design concept:
    1. provides an interactive CLI experience with clear user guidance.(this can be done 
       through with an addtion of UI library for the terminal which can make it look interactive)
    2. supports continuous searching while allowing users to exit easily. (here I can use the break as well to end the CLI tool)
    3. shoud be able to maintains a lightweight search for optimization of 
       performance using less memory history with configurable limits. (this is also why I used a limit for the history as well)
       (this should work like a token mostly, I hope it can do that as I am not going to search like 100 times)
    4. provides an input validation and real-time feedback(eg. help, correction 
       of this zip code if wrong). (this should be the easiest of them all to code interms of code complexity as well)

    workflow:
    step 1: load library dataset into memory. 
    step 2: start the session for user queries.
    step 3: process and validate ZIP code inputs.
    step 4: retrieve matching libraries and display results.
    step 5: maintain a rolling search history for user reference.
    step 6: additionly, integrate this feature of "full history" 
            which will give you the time stamp as well the entire history search 

'''


def main() -> None:
    # Show polished welcome screen
    welcome_text = pyfiglet.figlet_format("ChiLib", font="slant")
    console.print(f"[cyan]{welcome_text}[/]")
    console.print("Chicago Public Library Finder", style="bold blue", justify="center")
    
    try:
        with Progress() as progress:
            task = progress.add_task("[cyan]Initializing system...", total=1)
            libraries = load_libraries()
            progress.update(task, completed=1)
    except DataLoadError as e:
        console.print(f"[bold red]🚨 {str(e)}[/bold red]")
        return

    history = []
    
    while True:
        try:
            user_input = console.input("\n[bold yellow]📮 Enter ZIP code (or 'help'): [/bold yellow]").strip().lower()
            
            # this is a simple command handling for the user help 
            if user_input in ('exit', 'quit'):
                console.print("\n[bold magenta]✨ Thank you for using Chicago Library Finder![/bold magenta]\n")
                break
                
            if user_input == 'help':
                console.print("\n[bold]COMMAND MENU:[/bold]")
                console.print("\n[bold]COMMAND MENU[/bold]")
                console.print("  [cyan]help[/cyan]    - Show this menu")
                console.print("  [cyan]history[/cyan] - Recent searches (compact view)")
                console.print("  [cyan]full[/cyan]    - Detailed search history")
                console.print("  [cyan]exit[/cyan]    - Quit application\n")
                continue
            
            # this is where I can check if the user wants to see the history of the search
            if user_input.startswith(('history', 'full')):
                if not history:
                    console.print("[yellow]⚠️  No search history available[/yellow]")
                    continue
                
                if 'full' in user_input:
                    display_history_table(history)
                else:
                    display_history(history)
                continue

            # here using like an if statement I can check  the user's input and validate it
            # and make sure the numbers he inputed are right 
            # if not then tell them it is wrong and give out the right format for them to understand what the correct format is 
            if not Config.ZIP_REGEX.match(user_input):
                console.print(f"[red]❌ Invalid ZIP code format. Must be 5 digits (e.g. 60606)[/red]")
                continue

            # here I am supposed to execute library search 
            # this should be a simple search function which will search the library based on the user input Zip code
            with console.status(f"[bold green]🔍 Searching {user_input}...[/bold green]"):
                matching = [lib for lib in libraries if lib['ZIP'] == user_input]
                time.sleep(0.3)  # simulated search delay

            if not matching:
                console.print(f"[bold yellow]⚠️  No libraries found in ZIP {user_input}[/bold yellow]")
            else:
                console.print(f"[green]✅ Found {len(matching)} libraries:[/green]")
                search_time = datetime.now()
                for idx, lib in enumerate(matching, 1):
                    console.print(format_library(lib, idx))
                    history.append({'time': search_time, 'library': lib})
                
                # this should be able to maintain history limits for time complexity reasons 
                history = history[-Config.HISTORY_LIMIT:]

        except KeyboardInterrupt:
            console.print("\n[bold red]🚪 Exiting gracefully...[/bold red]")
            break

if __name__ == "__main__":
    main()