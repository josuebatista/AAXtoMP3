# The purpose of this convert_aax_to_mp3() is to convert AAX (or AAXC) files to common MP3, M4A, M4B, flac and ogg formats through a basic bash script frontend to FFMPEG.
# JRB - 2024-01-10

import subprocess
import os
import datetime

def convert_aax_to_mp3(audible_id, aax_file_path, real_time_output=False):
    # Calculates timestamp
    timestamp_now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

    # Determine the log file path
    log_file_path = os.path.splitext(aax_file_path)[0] + '-' + timestamp_now + '.log'

    # Construct the command
    command = [
        './AAXtoMP3',
        '-A', audible_id,
        '--chapter-naming-scheme', '$(echo "${title%%:*}" | sed "s/[^A-Za-z0-9 ]//g; s/ /_/g")-$(printf %0${#chaptercount}d $chapternum)',
        '-D', '$(echo "${title%%:*}" | sed "s/[^A-Za-z0-9 ]//g; s/ /_/g")', '-d',
        aax_file_path
    ]

    if real_time_output:
        # Use subprocess.Popen for real-time output
        with open(log_file_path, 'w') as log_file:
            try:
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

                # Display output in real-time
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        print(output.strip())
                        log_file.write(output)
                process.wait()
            except subprocess.CalledProcessError as e:
                print(f"Error occurred: {e}")
    else:
        # Use subprocess.run for non-interactive execution
        with open(log_file_path, 'w') as log_file:
            try:
                subprocess.run(command, check=True, stdout=log_file, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                print(f"Error occurred: {e}")

# Example usage
# convert_aax_to_mp3('your_audible_id', '/path/to/your/file.aax', real_time_output=True)
