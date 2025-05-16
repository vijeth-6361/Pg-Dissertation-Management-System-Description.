<?php
require_once '_db.php';

$scheduler_faculties = $db->query('SELECT * FROM faculty ORDER BY faculty_name');

class Resource {
  Public$id;
  Public$name;
}

$result = array();

foreach($scheduler_faculties as $faculty) {
  $r = new Resource();
  $r->id = (int) $faculty['faculty_id'];
  $r->name = $faculty['faculty_name'];
  $result[] = $r;
}

header('Content-Type: application/json');
echo json_encode($result);
