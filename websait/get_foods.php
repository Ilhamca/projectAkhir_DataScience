<?php
header('Content-Type: application/json');

// Read nutrition data
$data = [];
if (file_exists('nutrition_data.csv')) {
    $file = fopen('nutrition_data.csv', 'r');
    $headers = fgetcsv($file);
    
    while (($row = fgetcsv($file)) !== false) {
        $food = [];
        foreach ($headers as $i => $header) {
            $food[$header] = $row[$i];
        }
        $data[] = $food;
    }
    fclose($file);
}

echo json_encode($data);
?>
