<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistem Analisis Gizi Makanan Indonesia</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #C62828 0%, #E53935 50%, #FFFFFF 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            max-width: 1000px;
            width: 100%;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 50px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 15px;
        }
        
        .header p {
            font-size: 1.3em;
            opacity: 0.95;
        }
        
        .role-selection {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 40px;
            margin-top: 40px;
        }
        
        .role-card {
            background: white;
            border-radius: 20px;
            padding: 50px 40px;
            text-align: center;
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
            transition: all 0.4s ease;
            cursor: pointer;
            border: 4px solid transparent;
            position: relative;
            overflow: hidden;
        }
        
        .role-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.5s;
        }
        
        .role-card:hover::before {
            left: 100%;
        }
        
        .role-card:hover {
            transform: translateY(-15px) scale(1.05);
            box-shadow: 0 25px 60px rgba(0,0,0,0.4);
            border-color: #C62828;
        }
        
        .role-icon {
            font-size: 5em;
            margin-bottom: 20px;
            display: block;
        }
        
        .role-card h2 {
            color: #C62828;
            font-size: 2.2em;
            margin-bottom: 15px;
        }
        
        .role-card p {
            color: #666;
            font-size: 1.1em;
            line-height: 1.6;
            margin-bottom: 25px;
        }
        
        .role-card .features {
            text-align: left;
            margin: 20px 0;
            padding: 20px;
            background: #f5f5f5;
            border-radius: 10px;
        }
        
        .role-card .features li {
            margin: 10px 0;
            color: #555;
            font-size: 0.95em;
        }
        
        .role-card .btn {
            display: inline-block;
            padding: 15px 50px;
            background: linear-gradient(135deg, #C62828 0%, #D32F2F 100%);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-size: 1.2em;
            font-weight: 600;
            transition: all 0.3s;
            margin-top: 10px;
        }
        
        .role-card .btn:hover {
            background: linear-gradient(135deg, #B71C1C 0%, #C62828 100%);
            box-shadow: 0 8px 20px rgba(198, 40, 40, 0.4);
            transform: translateY(-2px);
        }
        
        @media (max-width: 768px) {
            .header h1 { font-size: 2em; }
            .header p { font-size: 1em; }
            .role-selection { grid-template-columns: 1fr; gap: 30px; }
            .role-card { padding: 40px 30px; }
            .role-icon { font-size: 4em; }
            .role-card h2 { font-size: 1.8em; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🇮🇩 Sistem Analisis Gizi Makanan Indonesia</h1>
            <p>Platform Lengkap untuk Analisis dan Manajemen Data Nutrisi</p>
        </div>
        
        <div class="role-selection">
            <div class="role-card" onclick="location.href='user.php'">
                <span class="role-icon">👤</span>
                <h2>Pengguna</h2>
                <p>Cari dan analisis kandungan gizi makanan Indonesia</p>
                <div class="features">
                    <ul>
                        <li>✓ Cari makanan dari database lengkap</li>
                        <li>✓ Lihat informasi nutrisi detail</li>
                        <li>✓ Analisis dengan berbagai model ML</li>
                        <li>✓ Interface mudah dan intuitif</li>
                    </ul>
                </div>
                <a href="user.php" class="btn">Masuk sebagai Pengguna</a>
            </div>
            
            <div class="role-card" onclick="location.href='admin.php'">
                <span class="role-icon">⚙️</span>
                <h2>Administrator</h2>
                <p>Kelola data, preprocessing, dan model machine learning</p>
                <div class="features">
                    <ul>
                        <li>✓ Data preprocessing & cleaning</li>
                        <li>✓ Konfigurasi model ML</li>
                        <li>✓ Visualisasi data & hasil</li>
                        <li>✓ Perbandingan performa model</li>
                    </ul>
                </div>
                <a href="admin.php" class="btn">Masuk sebagai Admin</a>
            </div>
        </div>
    </div>
</body>
</html>
