import os
import sys
import argparse
import modules.functions.metadata as metadata_handler
import modules.functions.database as database

file_types = ("wav", "flac", "mp3", "m4a")

parser = argparse.ArgumentParser()

parser.add_argument('--directory', '-d', help = "The directory to process (where the audio files are stored)", type = str)
parser.add_argument('--database', '-f', help = "The name of the database file to use, defaults to 'music'", type = str, default = "music")

# Print help if the user did not supply command arguments
if len(sys.argv) < 2:
    print(parser.format_help())
    exit(0)

args = parser.parse_args()

directory = args.directory
db_file = "{}.db3".format(args.database)

# Check if the directory exists
if not os.path.isdir(directory):
    print("Directory does not exist")
    exit(0)

# The file exists - delete it for now and start fresh - accumulative scan will follow (new files)
if os.path.isfile(db_file):
    os.remove(db_file)

# Create a fresh database file
database.migrate(db_file)

# This function will loop through the directories and work only with file_types
def scan_dir(baseDir):
    for entry in os.scandir(baseDir):
        if entry.is_file():
            if entry.name.endswith(file_types) and not entry.name.startswith('.'):
                full_path = os.path.join(baseDir, entry.name)
                data = {
                    'name': entry.name,
                    'location': full_path,
                    'directory': baseDir,
                    'extension': full_path.split(".")[-1]
                }
                yield data
        else:
            yield from scan_dir(entry.path)

try:
    # Count the files, just for reporting progress
    file_count = 0
    for entry in scan_dir(directory):
        file_count += 1

    print("Processing {} audio files".format(file_count))

    # Process the files
    start_count = 0
    for entry in scan_dir(directory):
        start_count += 1

        # Mutagen to get the metadata - replace soon with my own metadata program
        metadata = metadata_handler.create_from(entry)

        # The last inserted db entry id is needed for the foreign key
        file_id = database.store_file(db_file, entry)

        # Finally store the metadata with the audio stream details
        database.store_metadata(db_file, file_id, metadata)

        print ("{}/{} \r".format(start_count, file_count), end='', flush=True)
except KeyboardInterrupt:
    print("\nInterrupted! Cleaning up before exiting.")
finally:
    print("\nDone!\n", end='', flush=True)
