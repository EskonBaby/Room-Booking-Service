from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, time, datetime
from uuid import uuid4
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- Models ---
class Room(BaseModel):
    id: str
    name: str
    description: str
    capacity: int
    image_url: str


class BookingCreate(BaseModel):
    room_id: str
    user_name: str
    user_id: str
    booking_date: date
    start_time: time
    end_time: time


class Booking(BookingCreate):
    id: str

rooms_db = [
    Room(id="1", name="Beta Meeting Room", description="A modern and sleek meeting room for team standups and client calls.", capacity=6, image_url="https://images.unsplash.com/photo-1517502884422-41eaead166d4?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8MSUyMHRvJTIwMSUyMG1lZXRpbmclMjByb29tfGVufDB8fDB8fHww"),
    Room(id="2", name="Gamma Huddle", description="Small, quiet space perfect for focused work or quick discussions.", capacity=4, image_url="https://images.unsplash.com/photo-1577412647305-991150c7d163?auto=format&fit=crop&w=600&q=80"),
    Room(id="3", name="Delta Creative Space", description="An open, vibrant room with whiteboards and casual seating.", capacity=8, image_url="https://images.unsplash.com/photo-1524758631624-e2822e304c36?auto=format&fit=crop&w=600&q=80"),
    Room(id="4", name="Omega Executive", description="A luxurious private office for 1-on-1 confidential meetings.", capacity=2, image_url="https://images.unsplash.com/photo-1661169399398-dd271af8f651?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fDElMjB0byUyMDElMjBtZWV0aW5nJTIwcm9vbXxlbnwwfHwwfHx8MA%3D%3D"),
    Room(id="5", name="Alpha Boardroom", description="Large premium boardroom equipped with a projector and video conferencing.", capacity=12, image_url="https://media.istockphoto.com/id/1956811645/photo/conference-room-with-a-blank-empty-screen.webp?a=1&b=1&s=612x612&w=0&k=20&c=5EvpbryucIo-ExgbjutfwZZiH3O_ZwjYFTItQjQxS4o="),
]

bookings_db: List[Booking] = []


# --- Endpoints ---

@app.get("/api/rooms", response_model=dict)
def get_rooms_availability(booking_date: date, start_time: time, end_time: time):
    """Returns available and unavailable rooms based on requested time."""
    available = []
    unavailable = []

    for room in rooms_db:
        is_booked = False
        for b in bookings_db:
            if b.room_id == room.id and b.booking_date == booking_date:
                # Conflict logic: existing booking overlaps with requested time
                if max(start_time, b.start_time) < min(end_time, b.end_time):
                    is_booked = True
                    break

        if is_booked:
            unavailable.append(room)
        else:
            available.append(room)

    return {"available": available, "unavailable": unavailable}


@app.post("/api/bookings", response_model=Booking)
def create_booking(booking: BookingCreate):
    # 1. Validate past dates
    today = date.today()
    if booking.booking_date < today:
        raise HTTPException(status_code=400, detail="Cannot book in the past.")

    # 2. Validate time duration
    if booking.start_time >= booking.end_time:
        raise HTTPException(status_code=400, detail="End time must be after start time.")

    # 3. Check for double bookings
    for b in bookings_db:
        if b.room_id == booking.room_id and b.booking_date == booking.booking_date:
            if max(booking.start_time, b.start_time) < min(booking.end_time, b.end_time):
                raise HTTPException(status_code=400, detail="Room is already booked for this time.")

    new_booking = Booking(id=str(uuid4()), **booking.model_dump())
    bookings_db.append(new_booking)
    return new_booking


@app.get("/api/bookings", response_model=List[Booking])
def get_user_bookings():
    return bookings_db


@app.delete("/api/bookings/{booking_id}")
def cancel_booking(booking_id: str):
    global bookings_db
    bookings_db = [b for b in bookings_db if b.id != booking_id]
    return {"message": "Booking cancelled successfully"}