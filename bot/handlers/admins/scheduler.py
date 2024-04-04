from typing import List

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from filters.is_admin import IsAdmin
from utils.decorators import command_argument_required


router = Router()


@router.message(IsAdmin(), Command("jobs_count"))
async def handle_jobs_count_command(
    message: Message, scheduler: AsyncIOScheduler
) -> None:
    """Handles the /jobs_count command."""
    await message.answer(f"🔧 {len(scheduler.get_jobs())}")


@router.message(IsAdmin(), Command("jobs"))
async def handle_jobs_command(
    message: Message, scheduler: AsyncIOScheduler
) -> None:
    """Handles the /jobs command."""
    jobs: List[Job] = scheduler.get_jobs()
    text = ""
    for job in jobs:
        text += (
            f"🆔 <code>{job.id}</code> ({job.name})\n"
            f"📅 {job.trigger} ({job.next_run_time.strftime('%d.%m.%Y %H:%M')})\n\n"
        )
    await message.answer(text or "<i>No jobs found.</i>")


@router.message(IsAdmin(), Command("job"))
@command_argument_required()
async def handle_job_command(
    message: Message, scheduler: AsyncIOScheduler, job_id: str
) -> None:
    """Handles the /job command."""
    job: Job = scheduler.get_job(job_id)
    if job is None:
        return await message.answer("<i>Job not found.</i>")
    text = (
        f"🆔 <code>{job.id}</code>\n"
        f"📝 {job.name}\n"
        f"📅 {job.trigger} ({job.next_run_time.strftime('%d.%m.%Y %H:%M')})\n\n"
        f"🔧 {job.args}\n"
        f"🔧 {job.kwargs}"
    )
    await message.answer(text)
