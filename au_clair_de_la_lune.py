from pydub import AudioSegment
from pydub.generators import Sine
from pydub.playback import play
from math import pow
import keyboard 

base=32.70032
global note
note={'do':0,'sid':0,
      'dod':1,'reb':1,
      're':2,
      'red':3,'mib':3,
      'mi':4,'fab':4,
      'fa':5,'mid':5,
      'fad':6,'solb':6,
      'sol':7,
      'sold':8,'lab':8,
      'la':9,
      'lad':10,'sib':10,
      'si':11,'dob':11}
global tempo
tempo={'noire':1,'blanche':2,'ronde':4}

def getNoteFreq(noteName,noteOcta):
        return base*pow(2,(note[noteName]+12*noteOcta)/12)

def getSound(noteName,noteOcta,duration=1000):
        freq=getNoteFreq(noteName,noteOcta)
        print("freq: "+str(freq))
        play(Sine(freq).to_audio_segment(duration))

def playSong(noteList):
    for note in noteList:
        getSound(note[0],note[1],note[2])

def createSong(songList): #dirty
        noteTuple=songList[0]
        noteName=noteTuple[0]
        noteOcta=noteTuple[1]
        duration=noteTuple[2]
        freq=getNoteFreq(noteName,noteOcta)
        song=Sine(freq).to_audio_segment(duration)
        #
        for noteTuple in songList[1:]:
                noteName=noteTuple[0]
                noteOcta=noteTuple[1]
                duration=noteTuple[2]
                freq=getNoteFreq(noteName,noteOcta)
                song=song.append(Sine(freq).to_audio_segment(duration))
                song=song.append(Sine(0).to_audio_segment(100))
        return song

def auClairDeLaLune(oct,bpm):
        r=tempo['ronde']*(60000/bpm)
        b=tempo['blanche']*(60000/bpm)
        n=tempo['noire']*(60000/bpm)
        return [('sol',oct,n),('sol',oct,n),('sol',oct,n),('la',oct,n),('si',oct,b),('la',oct,b),('sol',oct,n),('si',oct,n),('la',oct,n),('la',oct,n),('sol',oct,r),
                  ('sol',oct,n),('sol',oct,n),('sol',oct,n),('la',oct,n),('si',oct,b),('la',oct,b),('sol',oct,n),('si',oct,n),('la',oct,n),('la',oct,n),('sol',oct,r),
                  ('la',oct,n),('la',oct,n),('la',oct,n),('la',oct,n),('mi',oct,b),('mi',oct,b),('la',oct,n),('sol',oct,n),('fa',oct,n),('mi',oct,n),('re',oct,r),
                  ('sol',oct,n),('sol',oct,n),('sol',oct,n),('la',oct,n),('si',oct,b),('la',oct,b),('sol',oct,n),('si',oct,n),('la',oct,n),('la',oct,n),('sol',oct,r)]

#createSong(auClairDeLaLune(2,200)).export("./auclairdelalune.mp3",format="mp3")
#playSong(auClairDeLaLune(2,300))


def testClavier():
        while True:#making a loop
                noteOcta=4
                duration=500
                if keyboard.is_pressed('a'):
                        getSound('do',noteOcta,duration)
                elif keyboard.is_pressed('z'):
                        getSound('re',noteOcta,duration)
                elif keyboard.is_pressed('e'):
                        getSound('mi',noteOcta,duration)
                elif keyboard.is_pressed('r'):
                        getSound('fa',noteOcta,duration)
                elif keyboard.is_pressed('t'):
                        getSound('sol',noteOcta,duration)
                elif keyboard.is_pressed('y'):
                        getSound('la',noteOcta,duration)
                elif keyboard.is_pressed('u'):
                        getSound('si',noteOcta,duration)
                elif keyboard.is_pressed('i'):
                        getSound('do',noteOcta+1,duration)
                elif keyboard.is_pressed('q'):
                        break
                else:
                        pass


play(createSong(auClairDeLaLune(3,150)))
#testClavier()
