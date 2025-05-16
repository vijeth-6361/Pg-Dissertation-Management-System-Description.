<?php
require_once '_db.php';

$json = file_get_contents('php://input');
$params = json_decode($json);

$session_id = session_id();

$stmt = $db->prepare("SELECT * FROM appointment JOIN faculty ON appointment.faculty_id = faculty.faculty_id WHERE (appointment_status = 'free' OR (appointment_status <> 'free' AND appointment_patient_session = :session)) AND NOT ((appointment_end <= :start) OR (appointment_start >= :end))");
$stmt->bindParam(':start', $params->start);
$stmt->bindParam(':end', $params->end);
$stmt->bindParam(":session", $session_id);
$stmt->execute();
$result = $stmt->fetchAll();

class Event {
  Public$id;
  Public$text;
  Public$start;
  Public$end;
  Public$resource;
  Public$tags;
}
class Tags {
  Public$status;
  Public$faculty;
}

$events = array();

foreach($result as $row) {
  $e = new Event();
  $e->id = (int) $row['appointment_id'];
  $e->text = "";
  $e->start = $row['appointment_start'];
  $e->end = $row['appointment_end'];
  $e->tags = new Tags();
  $e->tags->status = $row['appointment_status'];
  $e->tags->faculty = $row['faculty_name'];
  $events[] = $e;
}

header('Content-Type: application/json');
echo json_encode($events);
