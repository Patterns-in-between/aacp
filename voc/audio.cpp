#include "RtAudio.h"
#include "voc_demo.h"

RtAudio audio;

extern "C" {

static int callme( void * outputBuffer, void * inputBuffer, unsigned int numFrames,
            double streamTime, RtAudioStreamStatus status, void * data )
{
    SPFLOAT * output = (SPFLOAT *)outputBuffer;
    int i;
    voc_demo_d *vd = (voc_demo_d *)data;
    SPFLOAT tmp;

    for(i = 0; i < numFrames * 2; i+=2) {
        if(sp_voc_get_counter(vd->voc) == 0) {
            if(vd->mode == VOC_TONGUE) {
                sp_voc_set_tongue_shape(vd->voc, 
                        vd->tongue_pos, vd->tongue_diam);
            }
        }
        sp_voc_compute(vd->sp, vd->voc, &tmp);
        tmp *= vd->gain;
        output[i] = tmp;
        output[i + 1] = tmp;
    }
    
    return 0;
}

void voc_demo_setup(voc_demo_d *vd)
{
    unsigned int buffer_frames = 1024;
   
    RtAudio::DeviceInfo info; 
    RtAudio::StreamParameters iParams, oParams;
    info = audio.getDeviceInfo(audio.getDefaultOutputDevice());
    iParams.deviceId = audio.getDefaultInputDevice();
    iParams.nChannels = 0;
    iParams.firstChannel = 0;
    oParams.deviceId = audio.getDefaultOutputDevice();
    oParams.nChannels = 2;
    oParams.firstChannel = 0;
    
    RtAudio::StreamOptions options;
    
  
    audio.openStream( &oParams, NULL, 
            RTAUDIO_FLOAT32, info.preferredSampleRate, 
            &buffer_frames, &callme, vd, &options);
    audio.showWarnings( true );

    sp_create(&vd->sp);
    vd->sp->sr = info.preferredSampleRate;
    sp_voc_create(&vd->voc);
    sp_voc_init(vd->sp, vd->voc);
    vd->tract = sp_voc_get_tract_diameters(vd->voc);
    vd->tract_size= sp_voc_get_tract_size(vd->voc);
    vd->freq = sp_voc_get_frequency_ptr(vd->voc);
    vd->velum = sp_voc_get_velum_ptr(vd->voc);
    vd->tenseness = sp_voc_get_tenseness_ptr(vd->voc);

    *vd->freq = 160;
    vd->gain = 1;
    vd->mode = VOC_NONE;
}

void voc_demo_start(voc_demo_d *vd)
{
    audio.startStream();
}

void voc_demo_stop(voc_demo_d *vd)
{
    audio.stopStream();
}

void voc_demo_destroy(voc_demo_d *vd)
{
    sp_voc_destroy(&vd->voc);
    sp_destroy(&vd->sp);
}

}
