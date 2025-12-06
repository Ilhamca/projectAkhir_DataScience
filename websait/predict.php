<?php
header('Content-Type: application/json');

// Function to call Python prediction
function predictNutrition($calories, $proteins, $fat, $carbohydrate) {
    // Prepare input data
    $input = json_encode([
        'calories' => (float)$calories,
        'proteins' => (float)$proteins,
        'fat' => (float)$fat,
        'carbohydrate' => (float)$carbohydrate
    ]);
    
    // Save input to temporary file
    file_put_contents('temp_input.json', $input);
    
    // Call Python script
    $command = 'python predict_api.py';
    $output = shell_exec($command);
    
    // Parse output
    $prediction = json_decode($output, true);
    
    // Clean up
    if (file_exists('temp_input.json')) {
        unlink('temp_input.json');
    }
    
    return $prediction;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $calories = $_POST['calories'] ?? 0;
    $proteins = $_POST['proteins'] ?? 0;
    $fat = $_POST['fat'] ?? 0;
    $carbohydrate = $_POST['carbohydrate'] ?? 0;
    
    // Calculate additional metrics
    $total_macros = $proteins + $fat + $carbohydrate;
    $protein_ratio = $total_macros > 0 ? ($proteins / $total_macros) * 100 : 0;
    $fat_ratio = $total_macros > 0 ? ($fat / $total_macros) * 100 : 0;
    $carb_ratio = $total_macros > 0 ? ($carbohydrate / $total_macros) * 100 : 0;
    $calorie_density = $total_macros > 0 ? $calories / $total_macros : 0;
    
    // Get prediction
    $prediction = predictNutrition($calories, $proteins, $fat, $carbohydrate);
    
    // Determine category based on label name
    $label_name = $prediction['label_name'] ?? 'Buruk';
    $label = $prediction['label'] ?? 1;
    $category = '';
    $title = '';
    $description = '';
    
    // Map Indonesian labels to categories
    // Labels: 'Baik' (Good), 'Buruk' (Bad), 'Sangat Baik' (Very Good), 'Sangat Buruk' (Very Bad)
    if ($label_name == 'Sangat Baik') {
        $category = 'good';
        $title = '✅ Excellent Nutrition Profile (Sangat Baik)';
        $description = 'This food has an excellent macronutrient profile with outstanding nutritional value. Highly recommended for a healthy diet!';
    } elseif ($label_name == 'Baik') {
        $category = 'good';
        $title = '✅ Good Nutrition Profile (Baik)';
        $description = 'This food has a balanced macronutrient profile with good nutritional value. It\'s a healthy choice for your diet.';
    } elseif ($label_name == 'Buruk') {
        $category = 'bad';
        $title = '⚠️ Poor Nutrition Profile (Buruk)';
        $description = 'This food has a poor nutritional profile. Consider balancing it with other nutrient-rich foods or consume in moderation.';
    } else { // Sangat Buruk
        $category = 'worst';
        $title = '❌ Very Poor Nutrition Profile (Sangat Buruk)';
        $description = 'This food has a very poor nutritional profile. Consider healthier alternatives or limit consumption significantly.';
    }
    
    // Prepare response
    $response = [
        'category' => $category,
        'title' => $title,
        'description' => $description,
        'label' => $label,
        'confidence' => $prediction['confidence'] ?? 0,
        'nutrition' => [
            'calories' => round($calories, 2),
            'proteins' => round($proteins, 2),
            'fat' => round($fat, 2),
            'carbohydrate' => round($carbohydrate, 2),
            'total_macros' => round($total_macros, 2),
            'protein_ratio' => round($protein_ratio, 2),
            'fat_ratio' => round($fat_ratio, 2),
            'carb_ratio' => round($carb_ratio, 2),
            'calorie_density' => round($calorie_density, 2)
        ]
    ];
    
    echo json_encode($response);
} else {
    echo json_encode(['error' => 'Invalid request method']);
}
?>
