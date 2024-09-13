def parse_results(results):
    detections = []
    
    for result in results:
        for box in result.boxes:
            detection = {
                "class_name": result.names[int(box.cls)], 
                "confidence": float(box.conf),  
                "bounding_box": box.xyxy.tolist() 
            }
            detections.append(detection)
    
    return detections
