
# Import the SDK
import boto
import boto.elastictranscoder

arn='arn:aws:iam::262441097865:role/Elastic_Transcoder_Default_Role'
s3 = boto.connect_s3()
transcoder = boto.elastictranscoder.connect_to_region('us-west-1')

bucket_name = "taakestan"
bucket=s3.get_bucket(bucket_name)
folders=[]
jobMap={}

#presets process
taakPreset_h264_480p_100kbs_mp4_name='taakPreset_h264_480p_100kbs_mp4'
taakPreset_h264_480p_100kbs_mp4_command={"name":taakPreset_h264_480p_100kbs_mp4_name,"description":taakPreset_h264_480p_100kbs_mp4_name,"container":"mp4","video":{"Codec":"H.264", "CodecOptions":{"Profile":"baseline","Level":"3","MaxReferenceFrames":"3"},"KeyframesMaxDist":"200","FixedGOP":"false", "BitRate":"600","FrameRate":"10","Resolution":"640x480","AspectRatio":"4:3"},"audio":{"Codec":"AAC","CodecOptions":{"Profile":"AAC-LC"},"SampleRate":"22050","BitRate":"32","Channels":"1"},"thumbnails":{"Format":"png","Interval":"60","Resolution":"192x144", "AspectRatio":"4:3"}}

taakPreset_h264_480p_50kbs_mp4_name='taakPreset_h264_480p_50kbs_mp4'
taakPreset_h264_480p_50kbs_mp4_command={"name":taakPreset_h264_480p_50kbs_mp4_name,"description":taakPreset_h264_480p_50kbs_mp4_name,"container":"mp4","video":{"Codec":"H.264", "CodecOptions":{"Profile":"baseline","Level":"3","MaxReferenceFrames":"3"},"KeyframesMaxDist":"900","FixedGOP":"false", "BitRate":"300","FrameRate":"10","Resolution":"640x480","AspectRatio":"4:3"},"audio":{"Codec":"AAC","CodecOptions":{"Profile":"AAC-LC"},"SampleRate":"22050","BitRate":"16","Channels":"1"},"thumbnails":{"Format":"png","Interval":"60","Resolution":"192x144", "AspectRatio":"4:3"}}

taakPreset_vp8_480p_100kbs_webm_name='taakPreset_vp8_480p_100kbs_webm'
taakPreset_vp8_480p_100kbs_webm_command={"name":taakPreset_vp8_480p_100kbs_webm_name,"description": taakPreset_vp8_480p_100kbs_webm_name,"container":"webm","video":{"Codec":"vp8", "CodecOptions":{"Profile":"1"}, "KeyframesMaxDist":"200", "FixedGOP":"false", "BitRate":"600", "FrameRate":"10", "Resolution":"640x480", "AspectRatio":"4:3" },"audio": {"Codec":"vorbis", "SampleRate":"22050", "BitRate":"32", "Channels":"1" },"thumbnails": {"Format":"png", "Interval":"60", "Resolution":"192x144", "AspectRatio":"4:3"}}

taakPreset_vp8_480p_50kbs_webm_name='taakPreset_vp8_480p_50kbs_webm'
taakPreset_vp8_480p_50kbs_webm_command={"name":taakPreset_vp8_480p_50kbs_webm_name,"description": taakPreset_vp8_480p_50kbs_webm_name,"container":"webm","video":{"Codec":"vp8", "CodecOptions":{"Profile":"1"}, "KeyframesMaxDist":"900", "FixedGOP":"false", "BitRate":"300", "FrameRate":"10", "Resolution":"640x480", "AspectRatio":"4:3" },"audio": {"Codec":"vorbis", "SampleRate":"22050", "BitRate":"16", "Channels":"1" },"thumbnails": {"Format":"png", "Interval":"60", "Resolution":"192x144", "AspectRatio":"4:3"}}

preDefinedTaakPresets={}
preDefinedTaakPresets[taakPreset_h264_480p_100kbs_mp4_name]=taakPreset_h264_480p_100kbs_mp4_command
preDefinedTaakPresets[taakPreset_h264_480p_50kbs_mp4_name]=taakPreset_h264_480p_50kbs_mp4_command
preDefinedTaakPresets[taakPreset_vp8_480p_100kbs_webm_name]=taakPreset_vp8_480p_100kbs_webm_command
preDefinedTaakPresets[taakPreset_vp8_480p_50kbs_webm_name]=taakPreset_vp8_480p_50kbs_webm_command


#see what kind of custom presets we had before
list_presets = transcoder.list_presets()
custom_presetsName=[]
for idx,val in enumerate(list_presets['Presets']):
  if list_presets['Presets'][idx]['Type']=='Custom':
   custom_presetsName.append(list_presets['Presets'][idx]['Name']);
 

presets_name_Id_map={}
#get taak preset_ids if exist
for idx,key in enumerate(custom_presetsName):
 if key == taakPreset_h264_480p_100kbs_mp4_name:
  presets_name_Id_map[key]=list_presets['Presets'][idx]['Id'];
 if key == taakPreset_h264_480p_50kbs_mp4_name:
  presets_name_Id_map[key]=list_presets['Presets'][idx]['Id'];
 if key == taakPreset_vp8_480p_100kbs_webm_name:
  presets_name_Id_map[key]=list_presets['Presets'][idx]['Id'];
 if key == taakPreset_vp8_480p_50kbs_webm_name:
  presets_name_Id_map[key]=list_presets['Presets'][idx]['Id'];
 


#create taak presets if neccesary
for key,value in preDefinedTaakPresets.iteritems():
 if not key in custom_presetsName:
  presets_name_Id_map[key]=transcoder.create_preset(**value)['Preset']['Id'];
  
  

#pipeline process
#fill presets_name_Id_map
taakPreset_h264_480p_100kbs_mp4_id=presets_name_Id_map[taakPreset_h264_480p_100kbs_mp4_name]
taakPreset_h264_480p_50kbs_mp4_id=presets_name_Id_map[taakPreset_h264_480p_50kbs_mp4_name]
taakPreset_vp8_480p_100kbs_webm_id=presets_name_Id_map[taakPreset_vp8_480p_100kbs_webm_name]
taakPreset_vp8_480p_50kbs_webm_id=presets_name_Id_map[taakPreset_vp8_480p_50kbs_webm_name]


list_pipelines = transcoder.list_pipelines()
taak_pipeline_id='none'
taak_pipeline_name='taak_pipeline'

#get taak pipeline if exist
for idx,val in enumerate(list_pipelines['Pipelines']):
 if taak_pipeline_name == list_pipelines['Pipelines'][idx]['Name']:  
  taak_pipeline_id=list_pipelines['Pipelines'][idx]['Id'];
 

#create new pipeline if not exist
if taak_pipeline_id == 'none':
 pipeline_content_config={'Bucket':bucket.name,'Grantee Type':'Group','Grantee':'AllUsers','Access':'FULL_CONTROL','StorageClass':'ReducedRedundancy'};
 pipeline_thumbnail_config={'Bucket':bucket.name,'GranteeType':'Group','Grantee':'AllUsers','Access':'FULL_CONTROL','StorageClass':'ReducedRedundancy'};
 taak_pipeline_id=transcoder.create_pipeline(name=taak_pipeline_name, input_bucket=bucket.name, role=arn, content_config=pipeline_content_config, thumbnail_config=pipeline_thumbnail_config)['Pipeline']['Id'];

#job process
defaultOrginalFileName='/original.mp4'

output_h264_480p_100kbps_mp4='h264_480p_100kbps.mp4'
output_h264_480p_50kbps_mp4='h264_480p_50kbps.mp4'
output_vp8_480p_100kbps_webm='vp8_480p_100kbps.webm'
output_vp8_480p_50kbps_webm='vp8_480p_50kbps.webm'

#prepare folders
for key in bucket.list("webinars/","/"):
 if not key.name == 'webinars/':
  folders.append(key.name)
 

#find function to search in bucket.list
def find ( str , item):
 for key in bucket.list(item,"/"):
  if key.name == str:
   return 'true';

#fill JobMap 
for item in folders:
 if not find(item+output_h264_480p_100kbps_mp4,item) =='true':
  jobMap[item+output_h264_480p_100kbps_mp4]=taakPreset_h264_480p_100kbs_mp4_id;
 if not find(item+output_h264_480p_50kbps_mp4,item) =='true':
  jobMap[item+output_h264_480p_50kbps_mp4]=taakPreset_h264_480p_50kbs_mp4_id;
 if not find(item+output_vp8_480p_100kbps_webm,item) =='true':
  jobMap[item+output_vp8_480p_100kbps_webm]=taakPreset_vp8_480p_100kbs_webm_id;
 if not find(item+output_vp8_480p_50kbps_webm,item) =='true':
  jobMap[item+output_vp8_480p_50kbps_webm]=taakPreset_vp8_480p_50kbs_webm_id;
 



input_object={}
output_objects = []

#create Jobs
for key, presetId in jobMap.iteritems():
     keystr=str(key);
     input_key=keystr[0:keystr.rindex('/')]+defaultOrginalFileName;    
     input_object = {'Key':input_key,'FrameRate':'auto','Resolution':'auto','AspectRatio':'auto','Interlaced':'auto','Container':'auto'};
     output_objects = [{'Key':key,'PresetId':presetId,'Rotate':'auto','ThumbnailPattern':''}];  
     transcoder.create_job(taak_pipeline_id, input_name=input_object, outputs=output_objects);




