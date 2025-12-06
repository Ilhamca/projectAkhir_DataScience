<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analisis Gizi Makanan Indonesia</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #C62828 0%, #E53935 50%, #FFFFFF 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container { max-width: 1400px; margin: 0 auto; }
        
        header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
            background: linear-gradient(135deg, #B71C1C 0%, #D32F2F 100%);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            position: relative;
        }
        
        .back-btn {
            position: absolute;
            left: 20px;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(255,255,255,0.2);
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            transition: 0.3s;
        }
        
        .back-btn:hover {
            background: rgba(255,255,255,0.3);
        }
        
        header h1 { font-size: 2.8em; margin-bottom: 10px; text-shadow: 3px 3px 6px rgba(0,0,0,0.5); }
        header p { font-size: 1.2em; opacity: 0.95; }
        
        .search-section {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .search-input {
            width: 100%;
            padding: 15px;
            border: 3px solid #D32F2F;
            border-radius: 10px;
            font-size: 1.1em;
            margin-bottom: 15px;
        }
        
        .search-input:focus { outline: none; border-color: #B71C1C; box-shadow: 0 0 0 3px rgba(211, 47, 47, 0.1); }
        
        .model-selector {
            display: flex;
            gap: 10px;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .model-selector label {
            font-weight: 600;
            color: #C62828;
            min-width: 150px;
        }
        
        .model-selector select {
            flex: 1;
            padding: 12px;
            border: 2px solid #D32F2F;
            border-radius: 8px;
            font-size: 1em;
            background: white;
            cursor: pointer;
        }
        
        .food-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .food-card {
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
            transition: all 0.3s;
            cursor: pointer;
            border: 3px solid transparent;
        }
        
        .food-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.25);
            border-color: #D32F2F;
        }
        
        .food-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
            background: #f5f5f5;
        }
        
        .food-info { padding: 15px; }
        
        .food-name {
            font-size: 1.3em;
            font-weight: bold;
            color: #C62828;
            margin-bottom: 10px;
        }
        
        .food-nutrition {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 8px;
        }
        
        .food-label {
            display: inline-block;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin-top: 10px;
        }
        
        .label-sangat-baik { background: #4CAF50; color: white; }
        .label-baik { background: #8BC34A; color: white; }
        .label-buruk { background: #FF9800; color: white; }
        .label-sangat-buruk { background: #F44336; color: white; }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 1000;
            overflow-y: auto;
        }
        
        .modal-content {
            background: white;
            max-width: 900px;
            margin: 50px auto;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        }
        
        .modal-header {
            background: linear-gradient(135deg, #C62828 0%, #D32F2F 100%);
            color: white;
            padding: 25px;
            position: relative;
        }
        
        .modal-close {
            position: absolute;
            top: 15px;
            right: 20px;
            font-size: 2em;
            cursor: pointer;
            color: white;
            background: none;
            border: none;
        }
        
        .modal-body { padding: 30px; }
        
        .modal-image {
            width: 100%;
            max-height: 400px;
            object-fit: cover;
            border-radius: 15px;
            margin-bottom: 20px;
        }
        
        .nutrition-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 20px;
        }
        
        .nutrition-item {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #D32F2F;
        }
        
        .nutrition-label { font-size: 0.9em; color: #666; margin-bottom: 5px; }
        .nutrition-value { font-size: 1.3em; font-weight: bold; color: #C62828; }
        
        .btn-analyze {
            background: linear-gradient(135deg, #C62828 0%, #D32F2F 100%);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            margin-top: 20px;
            width: 100%;
            transition: all 0.3s;
        }
        
        .btn-analyze:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(198, 40, 40, 0.4);
        }
        
        .result-box {
            margin-top: 20px;
            padding: 20px;
            border-radius: 10px;
            display: none;
        }
        
        .result-box.show { display: block; }
        .loading { text-align: center; padding: 40px; color: #666; }
        .no-results { text-align: center; padding: 40px; color: #999; font-size: 1.2em; }
        
        @media (max-width: 768px) {
            .food-grid { grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); }
            .nutrition-grid { grid-template-columns: 1fr; }
            header h1 { font-size: 2em; }
            .back-btn { position: relative; left: 0; transform: none; display: block; margin-bottom: 15px; text-align: center; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <a href="index.php" class="back-btn">← Kembali</a>
            <h1>🇮🇩 Analisis Gizi Makanan Indonesia</h1>
            <p>Cari dan analisis kandungan gizi makanan tradisional Indonesia</p>
        </header>

        <div class="search-section">
            <input type="text" id="searchInput" class="search-input" 
                   placeholder="Cari makanan... (contoh: soto, rendang, ayam)" autocomplete="off">
            
            <div class="model-selector">
                <label for="modelSelect">Pilih Model Analisis:</label>
                <select id="modelSelect">
                    <option value="random_forest">Random Forest (Rekomendasi)</option>
                    <option value="naive_bayes">Naive Bayes</option>
                    <option value="kmeans">K-Means Clustering</option>
                    <option value="svm">SVM (Support Vector Machine)</option>
                </select>
            </div>
        </div>

        <div id="foodGrid" class="food-grid">
            <div class="loading">Memuat data makanan...</div>
        </div>
    </div>

    <div id="foodModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <button class="modal-close" onclick="closeModal()">&times;</button>
                <h2 id="modalTitle">Detail Makanan</h2>
            </div>
            <div class="modal-body">
                <img id="modalImage" class="modal-image" src="" alt="">
                <div id="modalInfo"></div>
            </div>
        </div>
    </div>

    <script>
        let foodsData = [];
        let selectedModel = 'random_forest';

        fetch('get_foods.php')
            .then(response => response.json())
            .then(data => {
                foodsData = data;
                displayFoods(data);
            })
            .catch(error => {
                document.getElementById('foodGrid').innerHTML = '<div class="no-results">Gagal memuat data makanan</div>';
            });

        document.getElementById('searchInput').addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const filtered = foodsData.filter(food => food.name.toLowerCase().includes(searchTerm));
            displayFoods(filtered);
        });

        document.getElementById('modelSelect').addEventListener('change', function(e) {
            selectedModel = e.target.value;
        });

        function displayFoods(foods) {
            const grid = document.getElementById('foodGrid');
            if (foods.length === 0) {
                grid.innerHTML = '<div class="no-results">Tidak ada makanan yang ditemukan</div>';
                return;
            }

            grid.innerHTML = foods.map(food => `
                <div class="food-card" onclick="showFoodDetail(${food.id})">
                    <img src="${food.image}" alt="${food.name}" class="food-image"
                         onerror="this.src='https://via.placeholder.com/280x200?text=${encodeURIComponent(food.name)}'">
                    <div class="food-info">
                        <div class="food-name">${food.name}</div>
                        <div class="food-nutrition"><strong>Kalori:</strong> ${parseFloat(food.calories).toFixed(1)} kcal</div>
                        <div class="food-nutrition"><strong>Protein:</strong> ${parseFloat(food.proteins).toFixed(1)}g | <strong>Lemak:</strong> ${parseFloat(food.fat).toFixed(1)}g</div>
                        <div class="food-nutrition"><strong>Karbohidrat:</strong> ${parseFloat(food.carbohydrate).toFixed(1)}g</div>
                        <span class="food-label ${getLabelClass(food.label)}">${food.label}</span>
                    </div>
                </div>
            `).join('');
        }

        function getLabelClass(label) {
            const map = {'Sangat Baik': 'label-sangat-baik', 'Baik': 'label-baik', 'Buruk': 'label-buruk', 'Sangat Buruk': 'label-sangat-buruk'};
            return map[label] || 'label-buruk';
        }

        function showFoodDetail(foodId) {
            const food = foodsData.find(f => f.id == foodId);
            if (!food) return;

            document.getElementById('modalTitle').textContent = food.name;
            document.getElementById('modalImage').src = food.image;
            
            document.getElementById('modalInfo').innerHTML = `
                <h3 style="color: #C62828; margin-bottom: 15px;">Informasi Gizi</h3>
                <div class="nutrition-grid">
                    <div class="nutrition-item"><div class="nutrition-label">Kalori</div><div class="nutrition-value">${parseFloat(food.calories).toFixed(1)} kcal</div></div>
                    <div class="nutrition-item"><div class="nutrition-label">Protein</div><div class="nutrition-value">${parseFloat(food.proteins).toFixed(1)} g</div></div>
                    <div class="nutrition-item"><div class="nutrition-label">Lemak</div><div class="nutrition-value">${parseFloat(food.fat).toFixed(1)} g</div></div>
                    <div class="nutrition-item"><div class="nutrition-label">Karbohidrat</div><div class="nutrition-value">${parseFloat(food.carbohydrate).toFixed(1)} g</div></div>
                    <div class="nutrition-item"><div class="nutrition-label">Klasifikasi Gizi</div><div class="nutrition-value"><span class="food-label ${getLabelClass(food.label)}">${food.label}</span></div></div>
                    <div class="nutrition-item"><div class="nutrition-label">Model Saat Ini</div><div class="nutrition-value" style="font-size: 1em;">${getModelName(selectedModel)}</div></div>
                </div>
                <button class="btn-analyze" onclick="analyzeFood(${food.id})">Analisis dengan ${getModelName(selectedModel)}</button>
                <div id="analysisResult" class="result-box"></div>
            `;

            document.getElementById('foodModal').style.display = 'block';
        }

        function getModelName(model) {
            const names = {'random_forest': 'Random Forest', 'naive_bayes': 'Naive Bayes', 'kmeans': 'K-Means Clustering', 'svm': 'SVM'};
            return names[model] || model;
        }

        function closeModal() {
            document.getElementById('foodModal').style.display = 'none';
        }

        async function analyzeFood(foodId) {
            const food = foodsData.find(f => f.id == foodId);
            if (!food) return;

            const resultDiv = document.getElementById('analysisResult');
            resultDiv.innerHTML = '<div class="loading">Menganalisis...</div>';
            resultDiv.classList.add('show');

            const formData = new FormData();
            formData.append('calories', food.calories);
            formData.append('proteins', food.proteins);
            formData.append('fat', food.fat);
            formData.append('carbohydrate', food.carbohydrate);
            formData.append('model', selectedModel);

            try {
                const response = await fetch('predict.php', {method: 'POST', body: formData});
                const result = await response.json();
                
                resultDiv.className = 'result-box show ' + getLabelClass(result.label_name || food.label);
                resultDiv.innerHTML = `<h3>${result.title}</h3><p>${result.description}</p><div style="margin-top: 15px;"><strong>Confidence:</strong> ${result.confidence}%</div>`;
            } catch (error) {
                resultDiv.className = 'result-box show label-sangat-buruk';
                resultDiv.innerHTML = '<h3>Error</h3><p>Gagal menganalisis makanan. Silakan coba lagi.</p>';
            }
        }

        window.onclick = function(event) {
            if (event.target === document.getElementById('foodModal')) closeModal();
        }
    </script>
</body>
</html>
