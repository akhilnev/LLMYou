import { NextResponse } from 'next/server'

export async function POST() {
  const apiUrl = 'https://llmyoubackend-production.up.railway.app/create_tavus_meeting'

  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      // Add body if needed: body: JSON.stringify({ /* your data here */ }),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    // Check if data.meeting_link exists, otherwise fall back to the entire data object
    const meetingLink = data.meeting_link || data
    return NextResponse.json({ meetingLink: meetingLink })
  } catch (error) {
    console.error('Error creating meeting:', error)
    return NextResponse.json({ error: 'Failed to create meeting' }, { status: 500 })
  }
}