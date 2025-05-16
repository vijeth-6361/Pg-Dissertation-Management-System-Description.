<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Upload & Management</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f4f4f4;
            text-align: center;
        }

        h1 {
            color: #333;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
        }

        h1 i {
            color: #4CAF50;
        }

        form {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            display: inline-block;
            margin-bottom: 20px;
        }

        input[type="file"] {
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            margin-bottom: 10px;
        }

        input[type="submit"] {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: 0.3s;
        }

        input[type="submit"]:hover {
            background-color: #45a049;
        }

        .file-list {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 15px;
            max-width: 800px;
            margin: 20px auto;
        }

        .file-item {
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            text-align: center;
            min-width: 250px;
            animation: fadeIn 0.5s ease-in-out;
        }

        .file-item a {
            display: inline-block;
            padding: 8px 12px;
            margin: 5px;
            text-decoration: none;
            border-radius: 5px;
            transition: 0.3s;
        }

        .download {
            background-color: #4CAF50;
            color: white;
        }

        .download:hover {
            background-color: #45a049;
        }

        .delete {
            background-color: #f44336;
            color: white;
        }

        .delete:hover {
            background-color: #d32f2f;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>

    <h1><i class="fas fa-file-upload"></i> File Upload & Management</h1>
    <form method="POST" action="upload.php" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <input type="submit" value="Upload">
    </form>

    <div class="file-list">
        <?php
        $files = scandir("uploads");
        for ($a = 2; $a < count($files); $a++) {
            echo '<div class="file-item">';
            echo '<p><i class="fas fa-file"></i> ' . $files[$a] . '</p>';
            echo '<a class="download" href="uploads/' . $files[$a] . '" download><i class="fas fa-download"></i> Download</a>';
            echo '<a class="delete" href="delete.php?name=uploads/' . $files[$a] . '"><i class="fas fa-trash"></i> Delete</a>';
            echo '</div>';
        }
        ?>
    </div>

</body>
</html>
