import argparse
import os
from converters.convs import MdProcessor

def main():
    parser = argparse.ArgumentParser(description="Markdown-to-HTML CLI App")
    subparsers = parser.add_subparsers(dest="command")

    # command parser
    cmd_parser = subparsers.add_parser("convert", help="command to convert markdown to html")
    cmd_parser.add_argument("input", type=str, help="existing input markdown file")
    cmd_parser.add_argument("output", type=str, help="new output HTML file")

    # Parse arguments
    args = parser.parse_args()

    # Map commands to functions
    if args.command == "convert":
        print(f"Converting markdown {args.input} to {args.output}")
        
        input_exists = os.path.exists(args.input)

        output_exists = os.path.exists(args.output)

        if not input_exists:
            raise FileNotFoundError(f"Input file '{args.input}' not found.")


        if output_exists:
            raise FileExistsError(f"Output file '{args.output}' already exists.")

        
        if input_exists and not output_exists:

            processor = MdProcessor()
            
            with open(args.input, 'r') as file:
            
                for line in file:
                    processor.check_append(line)
                    
                result = processor.finish()

                with open(args.output, "w") as file:
                    for line in result:
                        file.write(line + "\n")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()