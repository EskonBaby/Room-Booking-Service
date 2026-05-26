<template>
  <div class="min-h-screen bg-gray-50 text-gray-800 font-sans">
    <header class="bg-white border-b px-8 py-4 flex justify-between items-center">
      <div class="flex items-center space-x-2 font-bold text-xl text-blue-900">
        <span class="text-blue-500">🏢</span>
        <span>Room Reservation</span>
      </div>
      <nav class="flex space-x-4">
        <button @click="currentView = 'find'" :class="{'bg-blue-50 text-blue-700': currentView === 'find'}" class="px-4 py-2 rounded-lg font-medium flex items-center space-x-2">
          <span>📅</span> <span>Find Room</span>
        </button>
        <button @click="currentView = 'bookings'; fetchMyBookings()" :class="{'bg-blue-50 text-blue-700': currentView === 'bookings'}" class="px-4 py-2 rounded-lg font-medium flex items-center space-x-2">
          <span>🧾</span> <span>My Bookings</span>
        </button>
      </nav>
    </header>

    <main class="max-w-6xl mx-auto py-8 px-4">
      <div v-if="currentView === 'find'">
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center justify-between mb-8">
          <div class="flex space-x-4">
            <div>
              <label class="block text-sm text-gray-500 mb-1">📅 Date</label>
              <input type="date" v-model="search.date" :min="minSelectableDate" @change="fetchRooms" class="border rounded-lg px-4 py-2 bg-gray-50 w-48" />
            </div>
            <div>
              <label class="block text-sm text-gray-500 mb-1">🕒 Start Time</label>
              <select v-model="search.start" @change="handleTimeChange" class="border rounded-lg px-4 py-2 bg-gray-50 w-32 outline-none cursor-pointer">
                <option v-for="time in availableStartTimes" :key="time" :value="time">
                  {{ time }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm text-gray-500 mb-1">🕒 End Time</label>
              <select v-model="search.end" @change="fetchRooms" class="border rounded-lg px-4 py-2 bg-gray-50 w-32 outline-none cursor-pointer">
                <option v-for="time in availableEndTimes" :key="time" :value="time">
                  {{ time }}
                </option>
              </select>
            </div>
          </div>
          <div class="text-sm text-gray-500 text-right">
            Showing availability for <span class="font-bold text-gray-800">{{ search.date }}</span> from <br/>
            <span class="font-bold text-gray-800">{{ search.start }}</span> to <span class="font-bold text-gray-800">{{ search.end }}</span>
          </div>
        </div>

        <h2 class="text-xl font-bold flex items-center space-x-2 mb-4">
          <span class="text-green-500">✅</span>
          <span>Available Rooms ({{ availableRooms.length }})</span>
        </h2>
        <div class="grid grid-cols-3 gap-6 mb-8">
          <div v-for="room in availableRooms" :key="room.id" class="bg-white border border-gray-100 rounded-2xl shadow-sm overflow-hidden flex flex-col">
            <div class="h-40 bg-gray-200 relative">
               <img :src="room.image_url" :alt="room.name" class="w-full h-full object-cover" />
               <div class="absolute top-3 right-3 bg-green-100 text-green-700 text-xs font-bold px-3 py-1 rounded-full">Available</div>
            </div>

            <div class="p-5 flex-grow flex flex-col justify-between">
              <div>
                <h3 class="font-bold text-lg">{{ room.name }}</h3>
                <p class="text-sm text-gray-500 mt-2">{{ room.description }}</p>
              </div>
              <div class="mt-4 flex justify-between items-center">
                <span class="text-sm text-gray-600">👥 Up to {{ room.capacity }}</span>
                <button @click="bookRoom(room)" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition">Book Room</button>
              </div>
            </div>
          </div>
        </div>

        <h2 class="text-xl font-bold flex items-center space-x-2 mb-4 text-gray-400">
          <span class="text-red-500">❌</span>
          <span class="text-black">Unavailable Rooms ({{ unavailableRooms.length }})</span>
        </h2>
        <div class="grid grid-cols-3 gap-6 mb-8">
          <div v-for="room in unavailableRooms" :key="room.id" class="bg-gray-50 border border-gray-200 rounded-2xl shadow-sm overflow-hidden flex flex-col opacity-60 grayscale">
            <div class="h-40 bg-gray-300 relative">
               <img :src="room.image_url" :alt="room.name" class="w-full h-full object-cover" />
               <div class="absolute top-3 right-3 bg-red-100 text-red-700 text-xs font-bold px-3 py-1 rounded-full">Booked</div>
            </div>
            <div class="p-5 flex-grow flex flex-col justify-between">
              <div>
                <h3 class="font-bold text-lg text-gray-600">{{ room.name }}</h3>
                <p class="text-sm text-gray-500 mt-2">{{ room.description }}</p>
              </div>
              <div class="mt-4 flex justify-between items-center">
                <span class="text-sm text-gray-500">👥 Up to {{ room.capacity }}</span>
                <button disabled class="bg-gray-300 text-gray-500 cursor-not-allowed px-4 py-2 rounded-lg font-medium">Booked</button>
              </div>
            </div>
          </div>
        </div>
        </div>

      <div v-else>
         <h1 class="text-2xl font-bold mb-2">My Bookings</h1>
         <p class="text-gray-500 mb-8">Manage your upcoming room reservations</p>

         <div v-for="booking in myBookings" :key="booking.id" class="bg-white border rounded-xl p-5 mb-4 shadow-sm flex justify-between items-center">
            <div>
              <div class="flex items-center space-x-3 mb-2">
                <h3 class="font-bold text-lg">{{ getRoomName(booking.room_id) }}</h3>
                <span class="bg-blue-50 text-blue-600 text-xs px-2 py-1 rounded">Confirmed</span>
              </div>
              <div class="text-sm text-gray-500 flex space-x-4">
                <span>📅 {{ booking.booking_date }}</span>
                <span>🕒 {{ booking.start_time }} - {{ booking.end_time }}</span>
                <span>📍 Booked by {{ booking.user_name }} ({{ booking.user_id }})</span>
              </div>
            </div>
            <button @click="cancelBooking(booking.id)" class="text-red-600 bg-red-50 hover:bg-red-100 px-4 py-2 rounded-lg font-medium transition flex items-center space-x-2">
              <span>🗑️</span> <span>Cancel Booking</span>
            </button>
         </div>
      </div>
    </main>
  </div>
</template>

<script setup>
const getRoomName = (roomId) => {
  // Combine all currently fetched rooms to search for the ID
  const allRooms = [...availableRooms.value, ...unavailableRooms.value]
  const room = allRooms.find(r => r.id === roomId)
  return room ? room.name : `Room ID: ${roomId}`
}
import { ref, onMounted, computed, watch } from 'vue'

const currentView = ref('find')

// Keep a reference to actual 'today' for the time validation logic below
const actualToday = new Date().toISOString().split('T')[0]

const minSelectableDate = computed(() => {
  const now = new Date()
  if (now.getHours() >= 19) {
    const tomorrow = new Date(now)
    tomorrow.setDate(tomorrow.getDate() + 1)
    return tomorrow.toISOString().split('T')[0]
  }
  return actualToday
})

// Generate Time
const allTimeOptions = []
for (let h = 8; h <= 19; h++) {
  for (let m = 0; m < 60; m += 15) {
    const hour = h.toString().padStart(2, '0')
    const minute = m.toString().padStart(2, '0')
    const timeStr = `${hour}:${minute}`

    if (timeStr <= '19:00') {
      allTimeOptions.push(timeStr)
    }
  }
}

// Helper functions
const getInitialTimes = (targetDate) => {
  let validStarts = allTimeOptions.filter(time => time < '19:00')

  if (targetDate === actualToday) {
    const now = new Date()
    const currentHour = now.getHours().toString().padStart(2, '0')
    const currentMinute = now.getMinutes().toString().padStart(2, '0')
    const currentTimeStr = `${currentHour}:${currentMinute}`

    validStarts = validStarts.filter(time => time >= currentTimeStr)
  }

  const defaultStart = validStarts.length > 0 ? validStarts[0] : '08:00'

  const possibleEnds = allTimeOptions.filter(time => time > defaultStart)
  const defaultEnd = possibleEnds.length > 0 ? possibleEnds[0] : '19:00'

  return { start: defaultStart, end: defaultEnd, validStarts }
}

// Load initial values (with LocalStorage)
const savedDate = localStorage.getItem('room_date')
const savedStart = localStorage.getItem('room_start')
const savedEnd = localStorage.getItem('room_end')

// Check if the saved date is still valid (not yesterday)
const initialDate = (savedDate && savedDate >= minSelectableDate.value) ? savedDate : minSelectableDate.value

// Get the computed safe defaults
const safeDefaults = getInitialTimes(initialDate)

// Check if the saved start time is still in the future
const isSavedStartValid = savedStart && safeDefaults.validStarts.includes(savedStart)

const search = ref({
  date: initialDate,
  start: isSavedStartValid ? savedStart : safeDefaults.start,
  // Ensure the saved end time is strictly after the start time
  end: (isSavedStartValid && savedEnd && savedEnd > savedStart) ? savedEnd : safeDefaults.end
})

// Save change in Local Storage
watch(search, (newVal) => {
  localStorage.setItem('room_date', newVal.date)
  localStorage.setItem('room_start', newVal.start)
  localStorage.setItem('room_end', newVal.end)
}, { deep: true })

//  Filter Start Times (Max 18:45, and block past times if date is today)
const availableStartTimes = computed(() => {
  // A start time can never be 19:00, because the shortest meeting pushes the end time to 19:15
  let validStarts = allTimeOptions.filter(time => time < '19:00')

  if (search.value.date === actualToday) {
    const now = new Date()
    const currentHour = now.getHours().toString().padStart(2, '0')
    const currentMinute = now.getMinutes().toString().padStart(2, '0')
    const currentTimeStr = `${currentHour}:${currentMinute}`

    validStarts = validStarts.filter(time => time >= currentTimeStr)
  }

  return validStarts
})

// Filter End Times (Must be strictly greater than Start Time. Max is naturally 19:00)
const availableEndTimes = computed(() => {
  if (!search.value.start) return allTimeOptions
  return allTimeOptions.filter(time => time > search.value.start)
})

// Auto-correct conflicts when Start Time or Date changes
const handleTimeChange = () => {
  // If the new Start Time makes the End Time invalid, bump the End Time up
  if (search.value.end <= search.value.start) {
    const nextAvailableEnd = availableEndTimes.value[0]
    if (nextAvailableEnd) search.value.end = nextAvailableEnd
  }
  fetchRooms()
}

// Watch the date: if they change to 'today' and their current start time is in the past, reset it
watch(() => search.value.date, (newDate) => {
  if (newDate === actualToday && !availableStartTimes.value.includes(search.value.start)) {
    search.value.start = availableStartTimes.value[0] || '8:00'
    handleTimeChange()
  } else {
    fetchRooms()
  }
})

const availableRooms = ref([])
const unavailableRooms = ref([])
const myBookings = ref([])

const fetchRooms = async () => {
  try {
    const url = `http://127.0.0.1:9999/api/rooms?booking_date=${search.value.date}&start_time=${search.value.start}&end_time=${search.value.end}`
    const res = await fetch(url)

    if (!res.ok) throw new Error("Failed to fetch")

    const data = await res.json()
    availableRooms.value = data.available
    unavailableRooms.value = data.unavailable
  } catch (error) {
    console.error("Error fetching rooms:", error)
    alert("Could not connect to the backend. Is it running?")
  }
}

const bookRoom = async (room) => {
  const userName = prompt("Enter your Name:")
  const userId = prompt("Enter your Employee ID:")

  if(userName && userId) {
     const payload = {
        room_id: room.id,
        user_name: userName,
        user_id: userId,
        booking_date: search.value.date,
        start_time: search.value.start,
        end_time: search.value.end
     }

     try {
       const res = await fetch('http://127.0.0.1:9999/api/bookings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
        })
       if (!res.ok) {
         const errorData = await res.json()
         throw new Error(errorData.detail || "Booking failed")
       }

       alert('Room booked successfully!')
       fetchRooms() // Refresh the list
     } catch (error) {
       alert(error.message)
     }
  }
}

const fetchMyBookings = async () => {
   try {
     const res = await fetch('http://127.0.0.1:9999/api/bookings')
     if (!res.ok) throw new Error("Failed to fetch bookings")
     myBookings.value = await res.json()
   } catch(error) {
     console.error("Error fetching my bookings:", error)
   }
}
const cancelBooking = async (id) => {
   // Add a quick confirmation so users don't accidentally click it
   if (!confirm("Are you sure you want to cancel this booking?")) return;

   try {
     const res = await fetch(`http://127.0.0.1:9999/api/bookings/${id}`, {
       method: 'DELETE'
     });

     if (!res.ok) {
       throw new Error("Failed to cancel booking");
     }

     // Refresh the list immediately after a successful delete
     fetchMyBookings();
   } catch(error) {
     console.error("Error cancelling booking:", error);
     alert("Could not cancel the booking. Please try again.");
   }
}

onMounted(() => {
  fetchRooms()
})
</script>