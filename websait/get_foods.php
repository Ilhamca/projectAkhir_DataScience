<?php
header('Content-Type: application/json');
error_reporting(E_ALL);
ini_set('display_errors', 0);

// Get selected model from query parameter (default: random_forest)
$selectedModel = isset($_GET['model']) ? $_GET['model'] : 'random_forest';

// Validate model type
$validModels = ['random_forest', 'naive_bayes', 'svm', 'kmeans'];
if (!in_array($selectedModel, $validModels)) {
    $selectedModel = 'random_forest';
}

// Read nutrition data from original CSV
$data = [];
$originalFile = 'nutrition_data.csv';

if (!file_exists($originalFile)) {
    echo json_encode(['error' => 'Data file not found']);
    exit;
}

// First, read all foods from CSV
$file = fopen($originalFile, 'r');
$headers = fgetcsv($file);

while (($row = fgetcsv($file)) !== false) {
    $food = [];
    foreach ($headers as $i => $header) {
        $food[$header] = $row[$i];
    }
    $data[] = $food;
}
fclose($file);

// Prepare data for batch prediction
$predictionInput = [
    'foods' => array_map(function($food) {
        return [
            'id' => $food['id'] ?? '',
            'calories' => $food['calories'] ?? 0,
            'proteins' => $food['proteins'] ?? 0,
            'fat' => $food['fat'] ?? 0,
            'carbohydrate' => $food['carbohydrate'] ?? 0
        ];
    }, $data)
];

// Save to temp file
$tempFile = tempnam(sys_get_temp_dir(), 'predict_');
file_put_contents($tempFile, json_encode($predictionInput));

// Call Python script for REAL-TIME predictions using trained model
$pythonPath = 'C:/Users/RAFFY/anaconda3/python.exe';
$scriptPath = 'predict_batch.py';
$command = sprintf('"%s" %s %s "%s" 2>&1', $pythonPath, $scriptPath, $selectedModel, $tempFile);

$output = shell_exec($command);
unlink($tempFile);

// Parse predictions
$predictions = json_decode($output, true);

if (!$predictions || !isset($predictions['success']) || !$predictions['success']) {
    // Fallback to original labels if prediction fails
    foreach ($data as &$food) {
        $food['label'] = $food['label'] ?? 'Baik';
        $food['confidence'] = 0.0;
        $food['model_used'] = $selectedModel;
        $food['prediction_error'] = true;
    }
} else {
    // Merge predictions with food data
    $predictionMap = [];
    foreach ($predictions['predictions'] as $pred) {
        $predictionMap[$pred['id']] = $pred;
    }
    
    foreach ($data as &$food) {
        $foodId = $food['id'] ?? '';
        if (isset($predictionMap[$foodId])) {
            $pred = $predictionMap[$foodId];
            $food['original_label'] = $food['label'] ?? '';
            $food['label'] = $pred['label_name'];
            $food['model_prediction'] = $pred['prediction'];
            $food['confidence'] = $pred['confidence'];
            $food['model_used'] = $selectedModel;
            $food['real_time_prediction'] = true; // Flag to show it's real-time
        }
    }
}

echo json_encode($data);
?>
