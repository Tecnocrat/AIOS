using Microsoft.AspNetCore.Mvc;

[Route("api/services")]
[ApiController]
public class ServicesController : ControllerBase
{
    [HttpGet]
    public IActionResult GetServices()
    {
        return Ok(new { message = "Director API is running!" });
    }
}
