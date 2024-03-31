import sys
import re, operator, string
from optparse import OptionParser, OptionGroup
import time

VERSION = "0.0.3"

class StatsGen:
    def __init__(self):
        self.output_file = None

        # Filters
        self.minlength = None
        self.maxlength = None
        self.simplemasks = None
        self.charsets = None
        self.quiet = False
        self.debug = True

        # Stats dictionaries
        self.stats_length = dict()
        self.stats_simplemasks = dict()
        self.stats_advancedmasks = dict()
        self.stats_charactersets = dict()

        # Ignore stats with less than 1% coverage
        self.hiderare = False

        self.filter_counter = 0
        self.total_counter = 0

        # Minimum password complexity counters
        self.mindigit = None
        self.minupper = None
        self.minlower = None
        self.minspecial = None

        self.maxdigit = None
        self.maxupper = None
        self.maxlower = None
        self.maxspecial = None

    def analyze_password(self, password):
        """Analyze a single password and categorize its characteristics."""
        digit, lower, upper, special = 0, 0, 0, 0
        simplemask = []
        advancedmask_string = ""

        for letter in password:
            if letter.isdigit():
                digit += 1
                advancedmask_string += "?d"
                if not simplemask or simplemask[-1] != 'digit':
                    simplemask.append('digit')
            elif letter.islower():
                lower += 1
                advancedmask_string += "?l"
                if not simplemask or simplemask[-1] != 'lower':
                    simplemask.append('lower')
            elif letter.isupper():
                upper += 1
                advancedmask_string += "?u"
                if not simplemask or simplemask[-1] != 'upper':
                    simplemask.append('upper')
            else:  # Assuming any character that isn't upper/lower/digit is special
                special += 1
                advancedmask_string += "?s"
                if not simplemask or simplemask[-1] != 'special':
                    simplemask.append('special')

        # Convert the simple mask list into a string representation
        simplemask_string = '-'.join(simplemask) if simplemask else 'none'

        # Determine the character set based on the composition of the password
        charsets = []
        if digit > 0: charsets.append('digit')
        if lower > 0: charsets.append('lower')
        if upper > 0: charsets.append('upper')
        if special > 0: charsets.append('special')
        charset = "-".join(charsets) if charsets else 'none'

        # Calculate password policy adherence (this can be adjusted based on specific requirements)
        policy = {
            'digit': digit,
            'lower': lower,
            'upper': upper,
            'special': special
        }

        return len(password), charset, simplemask_string, advancedmask_string, policy


    def generate_stats(self, filename):
        """Generate password statistics."""
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\r\n')
                if not line: continue  # Skip empty lines

                try:
                    freq_str, password = line.split(':', 1)
                    freq = int(freq_str)  # Convert frequency to integer
                except ValueError:
                    print(f"Invalid line format: {line}")
                    continue  # Skip lines that don't match expected format

                # Analyze the password
                pass_length, charset, simplemask, advancedmask, policy = self.analyze_password(password)
                
                # Apply filters if they are set
                if self.minlength is not None and pass_length < self.minlength:
                    continue
                if self.maxlength is not None and pass_length > self.maxlength:
                    continue
                if self.charsets and charset not in self.charsets:
                    continue
                if self.simplemasks and simplemask not in self.simplemasks:
                    continue

                # Update the total and filtered counters
                self.total_counter += freq
                self.filter_counter += freq

                # Update stats dictionaries with the frequency of each attribute
                self.stats_length[pass_length] = self.stats_length.get(pass_length, 0) + freq
                self.stats_charactersets[charset] = self.stats_charactersets.get(charset, 0) + freq
                self.stats_simplemasks[simplemask] = self.stats_simplemasks.get(simplemask, 0) + freq
                self.stats_advancedmasks[advancedmask] = self.stats_advancedmasks.get(advancedmask, 0) + freq

                # Update minimum and maximum values for password complexity
                self.mindigit = min(policy['digit'], self.mindigit if self.mindigit is not None else policy['digit'])
                self.minlower = min(policy['lower'], self.minlower if self.minlower is not None else policy['lower'])
                self.minupper = min(policy['upper'], self.minupper if self.minupper is not None else policy['upper'])
                self.minspecial = min(policy['special'], self.minspecial if self.minspecial is not None else policy['special'])

                self.maxdigit = max(policy['digit'], self.maxdigit if self.maxdigit is not None else policy['digit'])
                self.maxlower = max(policy['lower'], self.maxlower if self.maxlower is not None else policy['lower'])
                self.maxupper = max(policy['upper'], self.maxupper if self.maxupper is not None else policy['upper'])
                self.maxspecial = max(policy['special'], self.maxspecial if self.maxspecial is not None else policy['special'])

        # Optionally, after processing all passwords, you can perform any final calculations 
        # or adjustments to the statistics before they are printed or saved.

    def print_stats(self):
        """Print password statistics."""
        print(f"[+] Analyzing {self.filter_counter*100/self.total_counter:.2f}% ({self.filter_counter}/{self.total_counter}) of passwords")
        print("    NOTE: Statistics below is relative to the number of analyzed passwords, not total number of passwords")
        print("\n[*] Length:")
        for length, count in sorted(self.stats_length.items(), key=operator.itemgetter(1), reverse=True):
            # Ensure count is an integer if it's not supposed to be a float
            print(f"[+] {length:25}: {count*100/self.filter_counter:02f}% ({int(count)})")  # Using 'f' for float formatting

        print("\n[*] Character-set:")
        for char, count in sorted(self.stats_charactersets.items(), key=operator.itemgetter(1), reverse=True):
            print(f"[+] {char:25}: {count*100/self.filter_counter:02f}% ({int(count)})")

        print("\n[*] Password complexity:")
        # Ensure these values are integers; explicitly convert if necessary
        print(f"[+]                     digit: min({self.mindigit if self.mindigit is not None else 0}) max({self.maxdigit if self.maxdigit is not None else 0})")
        print(f"[+]                     lower: min({self.minlower if self.minlower is not None else 0}) max({self.maxlower if self.maxlower is not None else 0})")
        print(f"[+]                     upper: min({self.minupper if self.minupper is not None else 0}) max({self.maxupper if self.maxupper is not None else 0})")
        print(f"[+]                   special: min({self.minspecial if self.minspecial is not None else 0}) max({self.maxspecial if self.maxspecial is not None else 0})")

        print("\n[*] Simple Masks:")
        for simplemask, count in sorted(self.stats_simplemasks.items(), key=operator.itemgetter(1), reverse=True):
            print(f"[+] {simplemask:25}: {count*100/self.filter_counter:02f}% ({int(count)})")

        print("\n[*] Advanced Masks:")
        for advancedmask, count in sorted(self.stats_advancedmasks.items(), key=operator.itemgetter(1), reverse=True):
            print(f"[+] {advancedmask:25}: {count*100/self.filter_counter:02f}% ({int(count)})")

        if self.output_file:
            for advancedmask, count in self.stats_advancedmasks.items():
                self.output_file.write(f"{advancedmask},{count}\n")

if __name__ == "__main__":

    header = f"""                       _ 
     StatsGen {VERSION}   | |
      _ __   __ _  ___| | _
     | '_ \\ / _` |/ __| |/ /
     | |_) | (_| | (__|   < 
     | .__/ \\__,_|\\___|_|\\_\\
     | |                    
     |_| iphelix@thesprawl.org
    \n"""

    parser = OptionParser(f"%prog [options] passwords.txt\n\nType --help for more options", version=f"%prog {VERSION}")

    filters = OptionGroup(parser, "Password Filters")
    filters.add_option("--minlength", dest="minlength", type="int", metavar="8", help="Minimum password length")
    filters.add_option("--maxlength", dest="maxlength", type="int", metavar="8", help="Maximum password length")
    filters.add_option("--charset", dest="charsets", help="Password charset filter (comma separated)", metavar="loweralpha,numeric")
    filters.add_option("--simplemask", dest="simplemasks", help="Password mask filter (comma separated)", metavar="stringdigit,allspecial")
    parser.add_option_group(filters)

    parser.add_option("-o", "--output", dest="output_file", help="Save masks and stats to a file", metavar="password.masks")
    parser.add_option("--hiderare", action="store_true", dest="hiderare", default=False, help="Hide statistics covering less than 1% of the sample")

    parser.add_option("-q", "--quiet", action="store_true", dest="quiet", default=False, help="Don't show headers.")
    (options, args) = parser.parse_args()

    # Print program header
    if not options.quiet:
        print(header)

    if len(args) != 1:
        parser.error("no passwords file specified")
        sys.exit(1)

    print("[*] Analyzing passwords in [%s]" % args[0])

    statsgen = StatsGen()

    if options.minlength is not None: statsgen.minlength = options.minlength
    if options.maxlength is not None: statsgen.maxlength = options.maxlength
    if options.charsets is not None: statsgen.charsets = [x.strip() for x in options.charsets.split(',')]
    if options.simplemasks is not None: statsgen.simplemasks = [x.strip() for x in options.simplemasks.split(',')]

    if options.hiderare: statsgen.hiderare = options.hiderare

    if options.output_file:
        print("[*] Saving advanced masks and occurrences to [%s]" % options.output_file)
        statsgen.output_file = open(options.output_file, 'w')

    statsgen.generate_stats(args[0])
    statsgen.print_stats()
