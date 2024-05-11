$(document).ready(function() {
    initializeEventListeners();
});

function initializeEventListeners() {
    // First, remove any previously bound event listeners to prevent duplication
    $(document).off('.poolGame');

    const svgContainer = $('#svg-container svg').get(0); // Direct reference to the SVG element
    let isDragging = false;
    let line = null;
    const cueBallRadius = 28; 

    // Function to get the cue ball's center dynamically
    function getCueBallCenter() {
        const cueBall = $('#WHITE_Ball', svgContainer);
        return {
            x: parseFloat(cueBall.attr('cx')),
            y: parseFloat(cueBall.attr('cy'))
        };
    }

    // Function to create a new line
    function createLine(x1, y1, x2, y2) {
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', x1);
        line.setAttribute('y1', y1);
        line.setAttribute('x2', x2);
        line.setAttribute('y2', y2);
        line.setAttribute('stroke', 'brown');
        line.setAttribute('stroke-width', 10);
        svgContainer.appendChild(line);
        return line;
    }

    // Convert screen coordinates to SVG coordinates
    function getRelativePosition(event, svgElement) {
        var point = svgElement.createSVGPoint();
        point.x = event.clientX;
        point.y = event.clientY;
        var CTM = svgElement.getScreenCTM();
        if (CTM) {
            return point.matrixTransform(CTM.inverse());
        }
        return { x: 0, y: 0 };
    }

    // Mouse down on the cue ball
    $(document).on('mousedown.poolGame', '#WHITE_Ball', function(event) {
        const cueBallCenter = getCueBallCenter();
        isDragging = true;
        event.preventDefault();
        line = createLine(cueBallCenter.x, cueBallCenter.y, cueBallCenter.x, cueBallCenter.y);
    });

    // Mouse move on the document
    $(document).on('mousemove.poolGame', function(event) {
        if (isDragging && line) {
            const newPos = getRelativePosition(event, svgContainer);
            line.setAttribute('x2', newPos.x);
            line.setAttribute('y2', newPos.y);
        }
    });

    // Mouse up on the document
    $(document).on('mouseup.poolGame', function(event) {
        isDragging = false;
        if (line) {
            const cueBallCenter = getCueBallCenter();
            const releasePos = getRelativePosition(event, svgContainer);
            let velocityX = (cueBallCenter.x - releasePos.x) * 5;
            let velocityY = (cueBallCenter.y - releasePos.y) * 5;

            // Constrain the velocity to a maximum magnitude
            velocityX = Math.max(Math.min(velocityX, 10000), -10000);
            velocityY = Math.max(Math.min(velocityY, 10000), -10000);

            svgContainer.removeChild(line);
            line = null;

            // AJAX call to make a shot
            $.ajax({
                url: '/make-shot',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ velocityX: velocityX, velocityY: velocityY }),
                success: function(response) {
                    console.log(response); // Log or handle the response from the server
                    fetchFramesAndAnimate();
                },
                error: function(xhr, status, error) {
                    console.error("Error making the shot:", status, error);
                }
            });

            function fetchFramesAndAnimate() {
                $.getJSON('/animateShot', function(data) {
                    animateFrames(data);
                }).fail(function(jqxhr, textStatus, error) {
                    const err = textStatus + ", " + error;
                    console.error("Request Failed: " + err);
                });
            }

            function animateFrames(frames) {
                const container = $('#svg-container');
                let frameIndex = 0;
                function nextFrame() {
                    if (frameIndex < frames.length) {
                        container.html(frames[frameIndex++]);
                        setTimeout(nextFrame, 125); 
                    } else {
                        // Fetch and apply the updated game state
                        fetchAndUpdateGameState();
                    }
                }
                nextFrame();
            }

            function fetchAndUpdateGameState() {
                $.ajax({
                    url: '/startGame.html',
                    type: 'POST',
                    success: function(response) {
                        $('body').html(response);
                        initializeEventListeners(); // Reapply event listeners to new elements
                    },
                    error: function(xhr, status, error) {
                        console.error("Error fetching startGame.html:", status, error);
                    }
                });
            }
        }
    });
}
