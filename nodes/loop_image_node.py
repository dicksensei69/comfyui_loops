import torch

class LoopImageNode:
    """
    A node that reorders a sequence of images into a loop
    by reversing the middle section and appending it to the original sequence.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
            },
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "execute"
    CATEGORY = "Image Processing"
    
    def execute(self, images):
        """
        Reorder images into a loop by reversing the middle section (excluding first and last)
        and appending to the original sequence.
        
        Args:
            images: A sequence of images
            
        Returns:
            The reordered sequence of images that forms a loop
        """
        # Check if we have enough images for meaningful looping
        if len(images) < 3:
            print("Warning: Image sequence has fewer than 3 images. Simple duplication used for looping.")
            # Simple duplication for very short sequences
            if len(images) == 1:
                return (images,)
            elif len(images) == 2:
                # For two images, just repeat the sequence
                return (torch.cat([images, images[0].unsqueeze(0)], dim=0),)
        
        # Main looping algorithm for sequences of 3 or more images
        original_sequence = images
        
        # Get the reversed middle section (exclude first and last)
        reversed_middle = original_sequence[1:-1].flip(dims=[0])
        
        # Create the loop: original + reversed (excluding duplicated last frame)
        looped_sequence = torch.cat([original_sequence, reversed_middle], dim=0)
        
        return (looped_sequence,)

NODE_CLASS_MAPPINGS = {
    "LoopImageNode": LoopImageNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoopImageNode": "Loop Image Sequence"
} 