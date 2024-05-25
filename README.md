# scriptApi_txt2mig-Stable-Diffusion

open webui-user.bat in stable diffusion  
  

and change

set COMMANDLINE_ARGS=

to 

set COMMANDLINE_ARGS=--api

(me set COMMANDLINE_ARGS=--opt-sdp-no-mem-attention --no-half-vae --opt-channelslast --api)
