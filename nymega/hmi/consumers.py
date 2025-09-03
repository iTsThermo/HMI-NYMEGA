import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import random

class GridConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.is_connected = True
        
        # KEY CHANGE: Initialize the state with some starting values.
        # These will be remembered for the duration of the connection.
        self.producer_values = [round(random.uniform(0.3, 0.7), 2) for _ in range(5)]

        await self.accept()
        # Start the periodic task
        asyncio.create_task(self.send_periodic_updates())

    async def disconnect(self, close_code):
        self.is_connected = False
        print("Grid WebSocket disconnected")

    async def send_periodic_updates(self):
        while self.is_connected:
            try:
                max_change = 0.15  # Controls how large the change can be
                
                for i in range(len(self.producer_values)):
                    # Calculate a small, random change
                    change = random.uniform(-max_change, max_change)
                    
                    # Apply the change to the current value
                    new_value = self.producer_values[i] + change
                    
                    # Clamp the value to ensure it stays between 0.0 and 1.0
                    self.producer_values[i] = max(0.0, min(1.0, new_value))

                # Prepare the data payload in the required format
                update_data = {
                    f'P{i}': round(self.producer_values[i], 2) for i in range(5)
                }

                await self.send(text_data=json.dumps(update_data))

                # Wait for 20secs
                await asyncio.sleep(20)

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break

        print("Stopping periodic updates.")