import { NextResponse } from 'next/server'

export async function POST() {
  const apiUrl = 'https://llmyoubackend-production.up.railway.app/create_tavus_meeting'
  const timeoutDuration = 120000 // 120 seconds (2 minutes)

  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), timeoutDuration)

  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      signal: controller.signal,
    })

    clearTimeout(timeoutId)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    const meetingLink = data.meeting_link || data
    return NextResponse.json({ meetingLink: meetingLink })
  } catch (error) {
    clearTimeout(timeoutId)
    console.error('Error creating meeting:', error)
    if (error instanceof Error && error.name === 'AbortError') {
      return NextResponse.json({ error: 'Request timed out' }, { status: 504 })
    }
    return NextResponse.json({ error: 'Failed to create meeting' }, { status: 500 })
  }
}