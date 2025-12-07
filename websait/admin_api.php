<?php
header('Content-Type: application/json');
error_reporting(E_ALL);
ini_set('display_errors', 0);

$action = $_GET['action'] ?? '';

try {
    switch ($action) {
        case 'load_data':
            loadData();
            break;
        case 'clean_data':
            cleanData();
            break;
        case 'transform_data':
            transformData();
            break;
        case 'train_model':
            trainModel();
            break;
        default:
            echo json_encode(['error' => 'Invalid action']);
    }
} catch (Exception $e) {
    echo json_encode(['error' => $e->getMessage()]);
}

function extractJSON($output) {
    // Remove any non-JSON content before and after JSON
    $output = trim($output);
    
    // Find the first { or [ and last } or ]
    $firstBrace = strpos($output, '{');
    $firstBracket = strpos($output, '[');
    
    $start = false;
    if ($firstBrace !== false && $firstBracket !== false) {
        $start = min($firstBrace, $firstBracket);
    } elseif ($firstBrace !== false) {
        $start = $firstBrace;
    } elseif ($firstBracket !== false) {
        $start = $firstBracket;
    }
    
    if ($start === false) {
        return json_encode(['error' => 'No valid JSON output']);
    }
    
    // Find corresponding closing brace/bracket
    $lastBrace = strrpos($output, '}');
    $lastBracket = strrpos($output, ']');
    
    $end = false;
    if ($lastBrace !== false && $lastBracket !== false) {
        $end = max($lastBrace, $lastBracket);
    } elseif ($lastBrace !== false) {
        $end = $lastBrace;
    } elseif ($lastBracket !== false) {
        $end = $lastBracket;
    }
    
    if ($end === false) {
        return json_encode(['error' => 'No valid JSON output']);
    }
    
    $json = substr($output, $start, $end - $start + 1);
    
    // Validate JSON
    json_decode($json);
    if (json_last_error() !== JSON_ERROR_NONE) {
        return json_encode(['error' => 'Invalid JSON: ' . json_last_error_msg(), 'raw_output' => $output]);
    }
    
    return $json;
}

function loadData() {
    $cmd = 'cd /d "' . __DIR__ . '" && C:/Users/RAFFY/anaconda3/python.exe admin_operations.py load_data 2>nul';
    $output = shell_exec($cmd);
    echo extractJSON($output);
}

function cleanData() {
    $input = json_decode(file_get_contents('php://input'), true);
    $options = json_encode($input, JSON_UNESCAPED_SLASHES);
    $tempFile = tempnam(sys_get_temp_dir(), 'clean_');
    file_put_contents($tempFile, $options);
    $cmd = 'cd /d "' . __DIR__ . '" && C:/Users/RAFFY/anaconda3/python.exe admin_operations.py clean_data_file "' . $tempFile . '" 2>nul';
    $output = shell_exec($cmd);
    unlink($tempFile);
    echo extractJSON($output);
}

function transformData() {
    $input = json_decode(file_get_contents('php://input'), true);
    $method = $input['method'] ?? 'standardize';
    $cmd = 'cd /d "' . __DIR__ . '" && C:/Users/RAFFY/anaconda3/python.exe admin_operations.py transform_data ' . $method . ' 2>nul';
    $output = shell_exec($cmd);
    echo extractJSON($output);
}

function trainModel() {
    $input = json_decode(file_get_contents('php://input'), true);
    $params = json_encode($input, JSON_UNESCAPED_SLASHES);
    $tempFile = tempnam(sys_get_temp_dir(), 'train_');
    file_put_contents($tempFile, $params);
    $cmd = 'cd /d "' . __DIR__ . '" && C:/Users/RAFFY/anaconda3/python.exe admin_operations.py train_model_file "' . $tempFile . '" 2>nul';
    $output = shell_exec($cmd);
    unlink($tempFile);
    echo extractJSON($output);
}
?>
