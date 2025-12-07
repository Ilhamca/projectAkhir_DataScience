<?php
header('Content-Type: application/json');

// Get selected model from query parameter (default: random_forest)
$selectedModel = isset($_GET['model']) ? $_GET['model'] : 'random_forest';

// Map numeric predictions to label names
function getLabelName($prediction) {
    $labels = [
        '0' => 'Sangat Buruk',
        '1' => 'Buruk',
        '2' => 'Baik',
        '3' => 'Sangat Baik'
    ];
    return isset($labels[$prediction]) ? $labels[$prediction] : $labels['2'];
}

// Read nutrition data with ML predictions
$data = [];
$predictionFile = 'nutrition_data_with_predictions.csv';
$originalFile = 'nutrition_data.csv';

// Use predictions file if available, otherwise fall back to original
$fileToUse = file_exists($predictionFile) ? $predictionFile : $originalFile;

if (file_exists($fileToUse)) {
    $file = fopen($fileToUse, 'r');
    $headers = fgetcsv($file);
    
    // Find prediction column indices
    $predictionColumn = $selectedModel . '_prediction';
    $confidenceColumn = $selectedModel . '_confidence';
    $predictionIndex = array_search($predictionColumn, $headers);
    $confidenceIndex = array_search($confidenceColumn, $headers);
    $originalLabelIndex = array_search('label', $headers);
    
    while (($row = fgetcsv($file)) !== false) {
        $food = [];
        foreach ($headers as $i => $header) {
            $food[$header] = $row[$i];
        }
        
        // Override label with ML model prediction if available
        if ($predictionIndex !== false && isset($row[$predictionIndex])) {
            $food['label'] = getLabelName($row[$predictionIndex]);
            $food['model_prediction'] = $row[$predictionIndex];
            $food['original_label'] = isset($row[$originalLabelIndex]) ? $row[$originalLabelIndex] : $food['label'];
        }
        
        // Add confidence score
        if ($confidenceIndex !== false && isset($row[$confidenceIndex])) {
            $food['confidence'] = round(floatval($row[$confidenceIndex]), 2);
        } else {
            $food['confidence'] = 100.0;
        }
        
        // Add model source info
        $food['model_used'] = $selectedModel;
        
        $data[] = $food;
    }
    fclose($file);
}

echo json_encode($data);
?>
