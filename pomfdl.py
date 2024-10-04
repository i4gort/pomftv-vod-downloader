import sys
import getopt
from modules import PomfTVDownloader, search_opt, url_opt, user_opt, help_message

##################################################################
#                       CONFIGURATION (?)                        #
##################################################################
#     Creates a folder from wherever the script is called        #
#      Beware it creates a folder with username inputted         #
#          Put the path you desire to store vods                 #
#     e.g. C:\Users\Anon\Videos\PomfTV OR ~/Videos/PomfTV        #
##################################################################

DEFAULT_DIR = ("./PomfTV")                                             

########################### MAIN #################################

if __name__ == "__main__":
    try:
        ############### Handle OPTIONS ###############
        try:
            argv = sys.argv[1:]
            opts, args = getopt.getopt(argv, "hU:u:s:d:", ["help", "url=",
                                                   "user=","search=", "dir="])
        except getopt.GetoptError as err:
            print(f"ERROR: {err}")
            print(help_message)
            sys.exit(-1)

        # Check if nothing is passed AKA Opts is empty
        if not opts:
            print(help_message)
            sys.exit(0)
        ############# END Handle OPTIONS #############

        handler = PomfTVDownloader(DEFAULT_DIR)
        for opt, arg in opts:
            if opt in ["-d", "--dir"]:
                DEFAULT_DIR = arg
                handler = PomfTVDownloader(DEFAULT_DIR)
                    
        for opt, arg in opts:
            if opt in ["-s", "--search"]:
                search_opt(arg, handler)
                sys.exit(0)
                            
            elif opt in ["-U", "--url"]:
                print(f"Downloading to: {DEFAULT_DIR}")
                url_opt(arg, handler)
                sys.exit(0)
                            
            elif opt in ["-u", "--user"]:
                print(f"Downloading to: {DEFAULT_DIR}")
                user_opt(arg, handler)
                sys.exit(0)
                            
            elif opt in ["--h", "-h", "--help"]:
                print(help_message)
                sys.exit(0)
    except KeyboardInterrupt:
        print("\nExiting")