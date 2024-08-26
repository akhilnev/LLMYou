import { NextResponse } from 'next/server'

export async function POST() {
  // Here you would typically call your actual meeting creation API
  const meetingLink = `https://meet.example.com/${Math.random().toString(36).substring(7)}`

  return NextResponse.json({ meetingLink })
}