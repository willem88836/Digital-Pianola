using System;
using System.IO;
using System.Threading;
using NAudio.Dsp;
using NAudio.MediaFoundation;
using NAudio.Wave;
using NAudio.Wave.SampleProviders;

namespace Pianola_Sheet_Converter
{
	/* 
		Stuff to look at: 
			http://archive.oreilly.com/oreillyschool/courses/data-structures-algorithms/soundFiles.html 
			https://cecm.indiana.edu/etext/digital_audio/chapter5_sample.shtml
			https://en.wikipedia.org/wiki/Piano_key_frequencies
		 */

	class Program
	{
		static void Main(string[] args)
		{
			string fileName = @"D:\\Users\\wille\\Documents\\Projects\\Tech-Projects\\GGJ2020-2\\Assets\\Audio\\background.mp3";


			AudioFileReader fileReader = new AudioFileReader(fileName);

			// number of audio samples per second. 
			int sampleRate = fileReader.WaveFormat.SampleRate;

			// number of bits in one sample.
			int bitsPerSample = fileReader.WaveFormat.BitsPerSample;

			// total number of samples.
			long numberOfSamples = fileReader.Length;
			int numberOfSamplesInt = (int)fileReader.Length;

			// total duration of the audio file.
			float duration = numberOfSamples / (float)sampleRate;

			// Don't know how this works, but it's probably correct. 
			// According to: Nyquist–Shannon sampling theorem. 
			int maximumlyDetectedFrequency = sampleRate / 2;


			long a = 0;
			byte[] buffer = new byte[bitsPerSample >> 3];

			while (a < numberOfSamples)
			{
				a += buffer.Length;
				fileReader.Read(buffer, 0, buffer.Length);
				long x = 0;

				for (int i = 0; i < buffer.Length; i++)
				{
					x += ((long)buffer[i]) << i;
				}

				if (x == 0)
					continue;

				Console.WriteLine(x);
				//Console.Beep((int)Math.Clamp((x), 37, 32767), 1000 / sampleRate);
			}











			////Console.WriteLine(sampleRate);
			////Console.WriteLine(bitsPerSample);


			//////byte[] buffer = new byte[sampleRate];
			//////fileReader.Read(buffer, 0, sampleRate);

			//////var bins = (sampleRate / 2) * sampleRate / numberOfSamplesInt;




			//////Console.WriteLine(numberOfSamples);
			//////Console.WriteLine((int)numberOfSamples);

			////fileReader.Read(buffer);



			//////fileReader.WaveFormat



			////IWavePlayer wo = new WaveOutEvent();
			////wo.Volume = 1;


			////wo.Init(fileReader);



			////wo.Play();
			////while(wo.PlaybackState == PlaybackState.Playing)
			////{

			////}

			Console.WriteLine("stopped playing");
		}




		public static void Prc()
		{
			string fileName = @"D:\Users\wille\Documents\Projects\Tech-Projects\GGJ2020-2\Assets\Audio\background.mp3";
			AudioFileReader fileIn = new AudioFileReader(fileName);

			long size = fileIn.Length;
			byte[] byteIn = new byte[size];
			fileIn.Read(byteIn);

			int rate = fileIn.WaveFormat.SampleRate;

			// http://archive.oreilly.com/oreillyschool/courses/data-structures-algorithms/soundFiles.html
		}






	}
}
