import cv2
from deepface import DeepFace
import time

def draw_face_info(frame, face):
    x, y, w, h = face['region'].values()
    gender = face['gender']
    age = face['age']
    emotion = face['dominant_emotion']
    
    # Dibujar rectángulo
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Texto informativo
    info = f"{gender}, {int(age)} años, {emotion}"
    cv2.putText(frame, info, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 2, cv2.LINE_AA)

def main():
    cap = cv2.VideoCapture(0)
    print("Presiona 'q' para salir.")
    
    frame_count = 0
    analysis_result = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        start_time = time.time()

        # Analizar cada 5 frames (puedes ajustar este valor)
        if frame_count % 5 == 0:
            try:
                analysis_result = DeepFace.analyze(
                    frame,
                    actions=['age', 'gender', 'emotion'],
                    enforce_detection=False
                )
            except Exception as e:
                print("Error:", e)
                analysis_result = []

        # Dibujar resultados
        if isinstance(analysis_result, list):
            for face in analysis_result:
                draw_face_info(frame, face)

        # Mostrar FPS
        end_time = time.time()
        fps = 1 / (end_time - start_time + 1e-6)
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 255, 255), 2)

        # Mostrar ventana
        cv2.imshow("Reconocimiento Facial en Tiempo Real", frame)

        # Salir con 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
