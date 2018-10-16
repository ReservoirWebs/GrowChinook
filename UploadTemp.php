
<?php
$target_dir = "uploads/temp/";
$target_file = $target_dir . basename($_FILES["filename"]["name"]);
$fileType = pathinfo($target_file,PATHINFO_EXTENSION);

if (move_uploaded_file($_FILES["filename"]["tmp_name"], $target_file)) {
        echo "The file ". basename( $_FILES["filename"]["name"]). " has been uploaded.";
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
?>
