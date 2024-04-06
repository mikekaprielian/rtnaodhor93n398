<?php
$url = "https://mediainfo.tf1.fr/mediainfocombo/L_LCI?format=hls";

function get_m3u8_url_video($url) {
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    $response = curl_exec($ch);
    curl_close($ch);

    preg_match('/(https:\/\/live.*?\.m3u8)/', $response, $matches);
    $matches = str_replace('index.m3u8', '', $matches);

    return $matches[0];
}

function get_m3u8_url_audio($url) {
    $ch2 = curl_init($url);
    curl_setopt($ch2, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch2, CURLOPT_FOLLOWLOCATION, true);
    $response = curl_exec($ch2);
    curl_close($ch2);

    preg_match('/(https:\/\/live.*?\.m3u8)/', $response, $matches_audio);
//    $matches_audio = str_replace('index.m3u8', '', $matches_audio);

    return $matches_audio[0];
}


$m3u8_url_video  = get_m3u8_url_video($url);

$m3u8_url_audio  = get_m3u8_url_audio($url);

//header('Content-Type: application/vnd.apple.mpegurl');

//echo "$m3u8_url_video";

echo "#EXTM3U\n";
echo "#EXT-X-VERSION:6\n";
echo "#EXT-X-INDEPENDENT-SEGMENTS\n";
echo '#EXT-X-STREAM-INF:BANDWIDTH=3192644,AVERAGE-BANDWIDTH=2890809,RESOLUTION=1280x720,FRAME-RATE=25.000,CODECS="avc1.4D401F,mp4a.40.2",SUBTITLES="subtitles",AUDIO="audio_0"'."\n";
echo "$m3u8_url_video"."index_1.m3u8\n";
echo '#EXT-X-STREAM-INF:BANDWIDTH=2207044,AVERAGE-BANDWIDTH=2010809,RESOLUTION=1024x576,FRAME-RATE=25.000,CODECS="avc1.4D401F,mp4a.40.2",SUBTITLES="subtitles",AUDIO="audio_0"'."\n";
echo "$m3u8_url_video"."index_2.m3u8\n";
echo '#EXT-X-STREAM-INF:BANDWIDTH=1591075,AVERAGE-BANDWIDTH=1460845,RESOLUTION=1024x576,FRAME-RATE=25.000,CODECS="avc1.4D401F,mp4a.40.2",SUBTITLES="subtitles",AUDIO="audio_0"'."\n";
echo "$m3u8_url_video"."index_3.m3u8\n";
echo '#EXT-X-STREAM-INF:BANDWIDTH=1098275,AVERAGE-BANDWIDTH=1020845,RESOLUTION=640x360,FRAME-RATE=25.000,CODECS="avc1.42C01E,mp4a.40.2",SUBTITLES="subtitles",AUDIO="audio_0"'."\n";
echo "$m3u8_url_video"."index_4.m3u8\n";
echo '#EXT-X-STREAM-INF:BANDWIDTH=605475,AVERAGE-BANDWIDTH=580845,RESOLUTION=416x234,FRAME-RATE=25.000,CODECS="avc1.42C00D,mp4a.40.2",SUBTITLES="subtitles",AUDIO="audio_0"'."\n";
echo "$m3u8_url_video"."index_5.m3u8\n";
echo '#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio_0",CHANNELS="2",NAME="fra",LANGUAGE="fra",DEFAULT=YES,AUTOSELECT=YES,URI="' . $m3u8_url_video . 'index_13_0.m3u8"'."\n";


//header("Location: $m3u8_url_video");
?>
