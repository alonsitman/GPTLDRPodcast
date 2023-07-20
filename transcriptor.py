from pydub import AudioSegment
from pydub.utils import make_chunks
import speech_recognition as sr
import math

def split_chunks_size(wav_filename, tmp_dir):
    myaudio = AudioSegment.from_file(wav_filename , "wav")
    channel_count = myaudio.channels        #Get channels
    sample_width = myaudio.sample_width     #Get sample width
    duration_in_sec = len(myaudio) / 1000   #Length of audio in sec
    sample_rate = myaudio.frame_rate

    # print ("sample_width=", sample_width )
    # print ("channel_count=", channel_count)
    # print ("duration_in_sec=", duration_in_sec) 
    # print ("frame_rate=", sample_rate)
    bit_rate = 16  #assumption , you can extract from mediainfo("test.wav") dynamically

    wav_file_size = (sample_rate * bit_rate * channel_count * duration_in_sec) / 8
    # print ("wav_file_size = ", wav_file_size)


    file_split_size = 10000000  # 10Mb OR 10, 000, 000 bytes
    # total_chunks =  wav_file_size // file_split_size

    #Get chunk size by following method #There are more than one ofcourse
    #for  duration_in_sec (X) -->  wav_file_size (Y)
    #So   whats duration in sec  (K) --> for file size of 10Mb
    #  K = X * 10Mb / Y

    chunk_length_in_sec = math.ceil((duration_in_sec * 10000000 ) /wav_file_size)   #in sec
    chunk_length_ms = chunk_length_in_sec * 1000
    chunks = make_chunks(myaudio, chunk_length_ms)

    #Export all of the individual chunks as wav files
    for i, chunk in enumerate(chunks):
        chunk_name = f"{tmp_dir}/" + "chunk{0}.wav".format(i)
        # print ("exporting", chunk_name)
        chunk.export(chunk_name, format="wav")

    # ToDo: no need for the entire list, just read wav-s by index
    return chunks


def transcript_chunks(chunks, txt_filename, tmp_dir):
    # open a file where we will concatenate
    # and store the recognized text
    fh = open(txt_filename, "w+")
        
    i = 0
    # process each chunk
    for i in range(len(chunks)):
        # the name of the newly created chunk
        filename = f'{tmp_dir}/' + 'chunk' + str(i) + '.wav'

        # print("Processing chunk "+str(i))

        # get the name of the newly created chunk
        # in the AUDIO_FILE variable for later use.
        file = filename

        # create a speech recognition object
        r = sr.Recognizer()

        # recognize the chunk
        with sr.AudioFile(file) as source:
            # remove this if it is not working
            # correctly.
            r.adjust_for_ambient_noise(source)
            audio_listened = r.listen(source)

        try:
            # try converting it to text
            rec = r.recognize_google(audio_listened)
            # write the output to the file.
            fh.write(rec+". ")

        # catch any errors.
        except sr.UnknownValueError:
            print("Could not understand audio")

        except sr.RequestError as e:
            print("Could not request results. check your internet connection")


def transcript_wav_chunked(wav_filename, txt_filename, tmp_dir):
    chunks = split_chunks_size(wav_filename, tmp_dir)
    transcript_chunks(chunks, txt_filename, tmp_dir)
    

def transcript_wav(wav_filename, txt_filename): 
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Open the audio file
    with sr.AudioFile(wav_filename) as source:
        audio_text = r.record(source)
    # Recognize the speech in the audio
    text = r.recognize_google(audio_text, language='en-US')

    with open(txt_filename, "w") as file:
        # Write to the file
        file.write(text)


def read_transcript(txt_filename):
    data = ""
    with open(txt_filename, 'r') as file:
        data = file.read().replace('\n', '')
    return data


def get_transcript(wav_filename, txt_filename, tmp_dir):
    transcript_wav_chunked(wav_filename, txt_filename, tmp_dir)
    transcript = read_transcript(txt_filename)
    return transcript

