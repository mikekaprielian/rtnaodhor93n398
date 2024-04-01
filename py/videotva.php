<?php

// Run the Python script and capture its output
$output = shell_exec('python3 https://raw.githubusercontent.com/mikekaprielian/rtnaodhor93n398/main/py/videotva.py');

// Forward the PHP page to the obtained link
header("Location: $output");

?>
