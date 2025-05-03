import torch
import unittest
from nodes.loop_image_node import LoopImageNode

class TestLoopImageNode(unittest.TestCase):
    def setUp(self):
        self.node = LoopImageNode()
        
    def test_single_image(self):
        """Test with a single image"""
        # Create a dummy single image (1x3x64x64)
        images = torch.randn(1, 3, 64, 64)
        result, = self.node.execute(images)
        
        # Result should be the same as input for a single image
        self.assertEqual(result.shape, images.shape)
        self.assertTrue(torch.equal(result, images))
        
    def test_two_images(self):
        """Test with two images"""
        # Create two dummy images (2x3x64x64)
        images = torch.randn(2, 3, 64, 64)
        result, = self.node.execute(images)
        
        # Result should be 3 images (original 2 + first one repeated)
        self.assertEqual(result.shape[0], 3)
        self.assertTrue(torch.equal(result[2], images[0]))
        
    def test_many_images(self):
        """Test with more than 2 images"""
        # Create 5 dummy images (5x3x64x64)
        images = torch.randn(5, 3, 64, 64)
        result, = self.node.execute(images)
        
        # Result should be 8 images (5 original + 3 reversed middle)
        self.assertEqual(result.shape[0], 8)
        
        # Check that the reversed middle section is correct
        # Original: [0,1,2,3,4]
        # Middle reversed: [3,2,1]
        # Final: [0,1,2,3,4,3,2,1]
        self.assertTrue(torch.equal(result[5], images[3]))
        self.assertTrue(torch.equal(result[6], images[2]))
        self.assertTrue(torch.equal(result[7], images[1]))
        
if __name__ == "__main__":
    unittest.main() 