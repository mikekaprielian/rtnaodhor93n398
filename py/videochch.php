<?php

// Run the Python script and capture its output
$output = shell_exec('python3 videochch.py');

// Forward the PHP page to the obtained link
header("Location: $output");

?>
