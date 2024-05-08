<?php

// URL to the text file containing potential M3U8 URLs
$filename = 'https://raw.githubusercontent.com/mikekaprielian/rtnaodhor93n398/main/txt/videotva.txt';

// Attempt to read the content of the file
$content = file_get_contents($filename);

// Check if the content was successfully fetched
if ($content === false) {
    die("Failed to retrieve the file.");
}

// Define the regex pattern to find M3U8 URLs
$pattern = '/https?:\/\/[\S]+?\.m3u8[\S]*/';  // Enhanced regex to capture entire URLs, including parameters

preg_match($pattern, $content, $matches);

header ("Location: $matches[0]");

//echo $matches[0];


?>
