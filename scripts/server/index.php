<?php
$file_name = __DIR__."/../../logs/latest.log";
$f_mod     = date('Y-m-d H:i:s', filemtime($file_name));
$log_file  = file_get_contents($file_name);
$lines     = preg_split("/\n/", $log_file);
$log       = '';

foreach($lines as $line)
{
    $line = preg_replace("/UUID of player (.*?) is ([a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+\-[a-z0-9]+\-)[a-z0-9]+/i", 'UUID of player $1 is $2************', $line);
    $line = preg_replace("/(.*?)(\[\/[0-9]+\.[0-9]+\.[0-9]+\.)[0-9]+(:[0-9]+\])/", '$1$2***$3', $line);
    $log .= "{$line}\n";
}

$output = "
<h1>Minecraft Server: Latest logs ({$f_mod})</h1>
<pre>
{$log}
</pre>";

echo $output;
