# Centralized entry point for command line interface
import argparse
from scripts import amazon_crawler_entrypoint

def main():
    parser = argparse.ArgumentParser(description='CLI for Fraudulent Sellers Amazon')
    parser.add_argument("-t", "--telegram", action="store", help="Obtain suspicios asins from telegram")
    parser.add_argument("-a", "--amazon", action="store_true", help="Run crawler to detect fraudulent sellers on amazon")
    args = parser.parse_args()

    if args.telegram:
        print("🛩️ TELEGRAM: extracting asins from messages")
    elif args.amazon:
        print("🌳 CRAWLER: detecting fraudulent sellers")
        amazon_crawler_entrypoint.run()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()