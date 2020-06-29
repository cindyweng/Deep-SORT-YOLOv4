import pandas as pd
from ast import literal_eval

files = ["/mnt/videos/Camera4_08-23-18_2020-02-24-320307_DTSL-07-50-16-09-00-13.csv"]
# files = ["/mnt/videos/Camera4_08-23-18_2020-02-24-320307_DTSL-07-50-16-09-00-13.csv", "/mnt/videos/Camera4_08-15-00_2020-02-24-320307 DTSL-07-50-16-09-00-13.csv",
#         "/mnt/videos/Camera4_08-12-32_2020-02-24-320307_DTSL-07-50-16-09-00-13.csv", "/mnt/videos/Camera1_08-23-38_2020-02-24-320307 DTSL-07-50-16-09-00-13.csv", 
#         "/mnt/videos/Camera1_08-15-28_2020-02-24-320307_DTSL-07-50-16-09-00-13.csv"]

for filename in files: 
	df = pd.read_csv(filename, sep=',')
	df.columns = df.columns.str.strip()
	df = df.groupby(['camera_id', 'frame_id', 'timestamp', 'seconds'])['track_id'].apply(list).reset_index(name='track_ids')

	filename2 = str(filename).strip(".csv") + "_agg.csv"
	df.to_csv(filename2, index=False, sep = ';')
	
	df = pd.read_csv(filename2, header = 0, sep = ';')
	cumulative = len(literal_eval(df.loc[[1]]['track_ids'].values[0]))
	camera_id = df.loc[[0]]['camera_id'].values[0]

	new_filename = str(filename).strip(".csv") + "_counts.csv"
	with open(new_filename, 'a') as f:
		f.write("camera_id,frame_id,timestamp,seconds,boarding,alighting,cumulative,count_now \n")
		
		timestamp = df.loc[[0]]['timestamp'].values[0]
		f.write("%s,%s,%s,%s,%s,%s,%s,%s\n" % (camera_id,0,timestamp,0,0,0,cumulative,cumulative))
		master_boarding_list=[]
		master_alighting_list=[]

		for i in range(20,len(df.index)):
			# print(i/len(df.index))
			print(df.loc[[i]]) 
			# print(df.loc[[i]]['timestamp'].values[0])
			frame_id = df.loc[[i]]['frame_id'].values[0]
			timestamp = df.loc[[i]]['timestamp'].values[0]
			seconds = df.loc[[i]]['seconds'].values[0]

			track_ids_before = []
			track_ids_now = []
			for n in range(11,20):
				track_ids_before.extend(literal_eval(df.loc[[i-n]]['track_ids'].values[0]))
				
			for k in range(0,10):
				track_ids_now.extend(literal_eval(df.loc[[i-k]]['track_ids'].values[0]))
			
			print(set(track_ids_before))
			print(set(track_ids_now))


			alighting = len(set(track_ids_before)-set(track_ids_now)-set(master_alighting_list))
			boarding = len(set(track_ids_now)-set(track_ids_before)-set(master_boarding_list))

			master_alighting_list.extend(list(set(track_ids_before)-set(track_ids_now)-set(master_alighting_list)))
			master_boarding_list.extend(list(set(track_ids_now)))
			master_alighting_list = list(set(master_alighting_list))
			master_boarding_list = list(set(master_boarding_list))

			count_now = len(set(track_ids_now))
			
			if (boarding + alighting > 0) and seconds >= 9.0:
				cumulative = cumulative - alighting + boarding
				# print(track_ids_before)
				# print(track_ids_now)
				# print(str(camera_id), str(frame_id), str(timestamp), str(boarding), str(alighting))
				f.write("%s,%s,%s,%s,%s,%s,%s,%s \n" % (camera_id,frame_id,timestamp,seconds,boarding,alighting,cumulative,count_now))
		f.close()
