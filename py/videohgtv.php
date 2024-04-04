<?php

// Define the log file path
//$log_file = 'EN-Showtime-errors.log';

// Run the Python script and capture its output and error
$output = shell_exec('python3 EN-HGTV.py 2>&1');

// Log the command output to a file
//file_put_contents($log_file, $output, FILE_APPEND);

// Forward the PHP page to the obtained link
header("Location: $output");

?>
